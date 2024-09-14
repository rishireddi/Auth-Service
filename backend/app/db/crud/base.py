# Built-in Dependencies
from typing import Any, Dict, Generic, List, Type, TypeVar, Union
from datetime import datetime, timezone

# Third-Party Dependencies
from sqlmodel import select, update, delete, func, and_, inspect, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.engine.row import Row
from sqlalchemy.sql import Join

# Local Dependencies
from app.db.crud.crud_helper import (
    _extract_matching_columns_from_schema,
    _extract_matching_columns_from_kwargs,
    _auto_detect_join_condition,
    _add_column_with_prefix,
)
from app.db.models.common import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)
UpdateSchemaInternalType = TypeVar("UpdateSchemaInternalType", bound=SQLModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=SQLModel)


class CRUDBase(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
        UpdateSchemaInternalType,
        DeleteSchemaType,
    ]
):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(self, db: AsyncSession, object: CreateSchemaType) -> ModelType:
        object_dict = object.model_dump()
        db_object: ModelType = self._model(**object_dict)
        db.add(db_object)
        await db.commit()
        return db_object

    async def get(
        self,
        db: AsyncSession,
        schema_to_select: Union[Type[SQLModel], List, None] = None,
        **kwargs: Any,
    ) -> Dict:
        to_select = _extract_matching_columns_from_schema(
            model=self._model, schema=schema_to_select
        )
        stmt = select(*to_select).filter_by(**kwargs)

        db_row = await db.exec(stmt)
        result: Row = db_row.first()
        if result is not None:
            out: dict = dict(result._mapping)
            return out

        return None

    async def exists(self, db: AsyncSession, **kwargs: Any) -> bool:
        to_select = _extract_matching_columns_from_kwargs(
            model=self._model, kwargs=kwargs
        )
        stmt = select(*to_select).filter_by(**kwargs).limit(1)

        result = await db.exec(stmt)
        return result.first() is not None

    async def count(self, db: AsyncSession, **kwargs: Any) -> int:
        if kwargs:
            conditions = [
                getattr(self._model, key) == value for key, value in kwargs.items()
            ]
            combined_conditions = and_(*conditions)
            count_query = (
                select(func.count())
                .select_from(self._model)
                .filter(combined_conditions)
            )
        else:
            count_query = select(func.count()).select_from(self._model)
        total_count: int = await db.scalar(count_query)

        return total_count

    async def get_multi(
        self,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        schema_to_select: Union[Type[SQLModel], List[Type[SQLModel]], None] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        to_select = _extract_matching_columns_from_schema(
            model=self._model, schema=schema_to_select
        )
        stmt = select(*to_select).filter_by(**kwargs).offset(offset).limit(limit)

        result = await db.exec(stmt)
        data = [dict(row) for row in result.mappings()]

        total_count = await self.count(db=db, **kwargs)

        return {"data": data, "total_count": total_count}

    async def get_joined(
        self,
        db: AsyncSession,
        join_model: Type[ModelType],
        join_prefix: str = None,
        join_on: Union[Join, None] = None,
        schema_to_select: Union[Type[SQLModel], List, None] = None,
        join_schema_to_select: Union[Type[SQLModel], List, None] = None,
        join_type: str = "left",
        **kwargs: Any,
    ) -> dict:
        if join_on is None:
            join_on = _auto_detect_join_condition(self._model, join_model)

        # Extract columns to select from primary model based on schema
        primary_select = _extract_matching_columns_from_schema(
            model=self._model, schema=schema_to_select
        )
        join_select = []

        # Extract columns to select from joined model based on schema or all columns if schema_to_select is not provided
        if join_schema_to_select:
            columns = _extract_matching_columns_from_schema(
                model=join_model, schema=join_schema_to_select
            )
        else:
            columns = inspect(join_model).c

        for column in columns:
            labeled_column = _add_column_with_prefix(column, join_prefix)
            if f"{join_prefix}{column.name}" not in [
                col.name for col in primary_select
            ]:
                join_select.append(labeled_column)

        # Build the select statement with the specified join type and join condition
        if join_type == "left":
            stmt = select(*primary_select, *join_select).outerjoin(join_model, join_on)
        elif join_type == "inner":
            stmt = select(*primary_select, *join_select).join(join_model, join_on)
        else:
            raise ValueError(
                f"Invalid join type: {join_type}. Only 'left' or 'inner' are valid."
            )

        # Apply additional filters based on kwargs
        for key, value in kwargs.items():
            if hasattr(self._model, key):
                stmt = stmt.where(getattr(self._model, key) == value)

        # Execute the statement and retrieve the result
        db_row = await db.exec(stmt)
        result: Row = db_row.first()
        if result:
            out: dict = dict(result._mapping)
            return out

        return None

    async def get_multi_joined(
        self,
        db: AsyncSession,
        join_model: Type[ModelType],
        join_prefix: str = None,
        join_on: Union[Join, None] = None,
        schema_to_select: Union[Type[SQLModel], List[Type[SQLModel]], None] = None,
        join_schema_to_select: Union[Type[SQLModel], List[Type[SQLModel]], None] = None,
        join_type: str = "left",
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if join_on is None:
            join_on = _auto_detect_join_condition(self._model, join_model)

        primary_select = _extract_matching_columns_from_schema(
            model=self._model, schema=schema_to_select
        )
        join_select = []

        if join_schema_to_select:
            columns = _extract_matching_columns_from_schema(
                model=join_model, schema=join_schema_to_select
            )
        else:
            columns = inspect(join_model).c

        for column in columns:
            labeled_column = _add_column_with_prefix(column, join_prefix)
            if f"{join_prefix}{column.name}" not in [
                col.name for col in primary_select
            ]:
                join_select.append(labeled_column)

        if join_type == "left":
            stmt = select(*primary_select, *join_select).outerjoin(join_model, join_on)
        elif join_type == "inner":
            stmt = select(*primary_select, *join_select).join(join_model, join_on)
        else:
            raise ValueError(
                f"Invalid join type: {join_type}. Only 'left' or 'inner' are valid."
            )

        for key, value in kwargs.items():
            if hasattr(self._model, key):
                stmt = stmt.where(getattr(self._model, key) == value)

        stmt = stmt.offset(offset).limit(limit)

        db_rows = await db.exec(stmt)
        data = [dict(row._mapping) for row in db_rows]

        total_count = await self.count(db=db, **kwargs)

        return {"data": data, "total_count": total_count}

    async def update(
        self,
        db: AsyncSession,
        object: Union[UpdateSchemaType, Dict[str, Any]],
        **kwargs: Any,
    ) -> None:

        if isinstance(object, dict):
            update_data = object
        else:
            update_data = object.model_dump(exclude_unset=True)

        if "updated_at" in update_data.keys():
            update_data["updated_at"] = datetime.now(timezone.utc)

        stmt = update(self._model).filter_by(**kwargs).values(update_data)

        await db.exec(stmt)
        await db.commit()

    async def db_delete(self, db: AsyncSession, **kwargs: Any) -> None:
        stmt = delete(self._model).filter_by(**kwargs)
        await db.exec(stmt)
        await db.commit()

    async def delete(self, db: AsyncSession, db_row: Row = None, **kwargs: Any) -> None:
        db_row = db_row or await self.exists(db=db, **kwargs)
        if db_row:
            if "is_deleted" in self._model.__table__.columns:
                object_dict = {
                    "is_deleted": True,
                    "deleted_at": datetime.now(timezone.utc),
                }
                stmt = update(self._model).filter_by(**kwargs).values(object_dict)

                await db.exec(stmt)
                await db.commit()

            else:
                stmt = delete(self._model).filter_by(**kwargs)
                await db.exec(stmt)
                await db.commit()
