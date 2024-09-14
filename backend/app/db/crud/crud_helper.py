# Built-in Dependencies
from typing import Any, List, Type, Union, Optional

# Third-Party Dependencies
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql.elements import Label
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.schema import Column
from sqlmodel import inspect
from pydantic import BaseModel

# Local Dependencies
from app.db.models.common import Base


def _extract_matching_columns_from_schema(
    model: Type[Base], schema: Union[Type[BaseModel], list, None]
) -> List[Any]:
    column_list = list(model.__table__.columns)
    if schema is not None:
        if isinstance(schema, list):
            schema_fields = schema
        else:
            schema_fields = schema.model_fields.keys()

        column_list = []
        for column_name in schema_fields:
            if hasattr(model, column_name):
                column_list.append(getattr(model, column_name))

    return column_list


def _extract_matching_columns_from_kwargs(model: Type[Base], kwargs: dict) -> List[Any]:
    if kwargs is not None:
        kwargs_fields = kwargs.keys()
        column_list = []
        for column_name in kwargs_fields:
            if hasattr(model, column_name):
                column_list.append(getattr(model, column_name))

    return column_list


def _extract_matching_columns_from_column_names(
    model: Type[Base], column_names: list
) -> List[Any]:
    column_list = []
    for column_name in column_names:
        if hasattr(model, column_name):
            column_list.append(getattr(model, column_name))

    return column_list


def _auto_detect_join_condition(
    base_model: Type[DeclarativeMeta], join_model: Type[DeclarativeMeta]
) -> Optional[ColumnElement]:

    fk_columns = [col for col in inspect(base_model).c if col.foreign_keys]
    join_on = next(
        (
            base_model.__table__.c[col.name]
            == join_model.__table__.c[list(col.foreign_keys)[0].column.name]
            for col in fk_columns
            if list(col.foreign_keys)[0].column.table == join_model.__table__
        ),
        None,
    )

    if join_on is None:
        raise ValueError(
            "Could not automatically determine join condition. Please provide join_on."
        )

    return join_on


def _add_column_with_prefix(column: Column, prefix: Optional[str]) -> Label:
    column_label = f"{prefix}{column.name}" if prefix else column.name
    return column.label(column_label)
