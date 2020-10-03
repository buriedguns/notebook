from contextlib import closing
import json

import requests
import sqlite3


def execute(*sql, get_id=False):
	with closing(sqlite3.connect("sample.db")) as connection:
		cur = connection.cursor()
		try:
			cur.execute(*sql)
			connection.commit()
		except Exception as exc:
			print(exc)
		if cur.description:
			return cur.fetchall()
		if get_id:
			return cur.lastrowid


def request(request_type, url, json_data=""):
	type_of_request = {
		"get": requests.get,
		"post": requests.post,
		"put": requests.put,
		"delete": requests.delete,
		"patch": requests.patch,
	}.get(request_type)
	response = None
	response_body = None
	try:
		response = type_of_request(url, json=json_data)
		response_body = json.loads(response.content)
	except json.decoder.JSONDecodeError:
		return response.status_code, response_body
	return response.status_code, response_body


def check_get_all(resp_code, resp_body):
	raw_info = execute("SELECT * FROM phonebook")
	expected_response = []
	for i in raw_info:
		data = {
			"id": i[0],
			"name": i[1],
			"phone": i[2]
		}
		expected_response.append(data)

	assert resp_code == 200
	assert resp_body == expected_response


def check_search(name, resp_body):
	expected_response = {
		"id": execute("SELECT id FROM phonebook WHERE name = 'TEST_USER'")[0][0],
		"name": "TEST_USER",
		"phone": "+79998887766"
	}

	cases = {
		"TEST_USER": [expected_response],
		"test_user": [expected_response],
		"nonexistent": []
	}

	assert resp_body == cases[name]


def check_add_phone(body, resp_body):
	expected_response = {
		"id": execute(f"""SELECT id FROM phonebook WHERE name = '{body["name"]}'""")[0][0],
		"name": body.get("name"),
		"phone": body.get("phone")
	}
	assert "message" in resp_body
	assert resp_body.get("phone_info") == expected_response
	assert execute(f"""SELECT id FROM phonebook WHERE name = '{body["name"]}' AND phone = '{body["phone"]}'""")[0][0]


def check_remove_phone(resp_code, phone_id):
	assert resp_code == 200
	assert not execute(f"SELECT * FROM phonebook WHERE id = '{phone_id}'")
