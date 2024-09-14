{
	"info": {
		"_postman_id": "e20e9fdc-94d0-46ea-8749-4ffb9dddbabd",
		"name": "Auth Service",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "34971090"
	},
	"item": [
		{
			"name": "http://127.0.0.1:9000/users/change-role?user_email=developer@gmail.com&new_role=100",
			"request": {
				"method": "PATCH",
				"header": [],
				"url": {
					"raw": "http://127.0.0.1:9000/users/change-role?user_email=developer@gmail.com&new_role=100",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "9000",
					"path": [
						"users",
						"change-role"
					],
					"query": [
						{
							"key": "user_email",
							"value": "developer@gmail.com"
						},
						{
							"key": "new_role",
							"value": "100"
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "http://127.0.0.1:9000/users/count-by-role?role=100",
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "http://127.0.0.1:9000/users/count-by-role?role=100",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "9000",
					"path": [
						"users",
						"count-by-role"
					],
					"query": [
						{
							"key": "role",
							"value": "100",
							"description": "100"
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "http://127.0.0.1:9000/members/delete_member?memberName=invite1",
			"request": {
				"method": "DELETE",
				"header": [],
				"url": {
					"raw": "http://127.0.0.1:9000/members/delete_member?memberName=invite1",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "9000",
					"path": [
						"members",
						"delete_member"
					],
					"query": [
						{
							"key": "memberName",
							"value": "invite1"
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "http://127.0.0.1:9000/members/invite-member",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n  \"org_id\": \"3fddb01a-f2b7-4d35-9b51-796692407597\",\n  \"user_id\": \"833fed74-94db-46ad-90d2-414f77379bb7\",\n  \"role_id\": \"ca08dd05-5921-4c42-9743-73c557121acd\",\n  \"memberStatus\": 1,\n  \"memberSettings\": {},\n  \"memberName\": \"invite1\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://127.0.0.1:9000/members/invite-member",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "9000",
					"path": [
						"members",
						"invite-member"
					]
				}
			},
			"response": []
		},
		{
			"name": "http://127.0.0.1:9000/auth/change-password",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n  \"current_password\": \"developer\",\n  \"new_password\": \"developer123\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://127.0.0.1:9000/auth/change-password",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "9000",
					"path": [
						"auth",
						"change-password"
					]
				}
			},
			"response": []
		},
		{
			"name": "http://127.0.0.1:9000/auth/login",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n  \"email\": \"developer@gmail.com\",\n  \"password\": \"developer\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://127.0.0.1:9000/auth/login",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "9000",
					"path": [
						"auth",
						"login"
					]
				}
			},
			"response": []
		},
		{
			"name": "http://127.0.0.1:9000/users/signup",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n  \"organizationName\": \"Hello World Developers\",\n  \"organizationStatus\": 0,\n  \"organizationPersonal\": false,\n  \"organizationSettings\": {},\n  \"user_role\": 100,\n  \"email\": \"developer@gmail.com\",\n  \"userProfile\": {},\n  \"userStatus\": 0,\n  \"userSettings\": {},\n  \"password\": \"developer\",\n  \"memberName\": \"developer\",\n  \"memberStatus\": 0\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://127.0.0.1:9000/users/signup",
					"protocol": "http",
					"host": [
						"127",
						"0",
						"0",
						"1"
					],
					"port": "9000",
					"path": [
						"users",
						"signup"
					]
				}
			},
			"response": []
		}
	]
}