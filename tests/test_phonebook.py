import pytest

from .utils import (
	request,
	execute,
	check_get_all,
	check_search,
	check_add_phone,
	check_remove_phone
)

host = "http://127.0.0.1:5000"


class TestPhonebook:

	def test_get_all_phones(self, phonebook_fixture):
		resp_code, resp_body = request(
			"get",
			host+'/get-all'
		)
		check_get_all(resp_code, resp_body)

	@pytest.mark.parametrize("name, expected_code", [
		("TEST_USER", 200),
		("test_user", 200),
		("nonexistent", 200)
	])
	def test_search_phone(self, name, expected_code):
		resp_code, resp_body = request(
			"get",
			host + f'/search/{name}'
		)
		assert resp_code == expected_code
		check_search(name, resp_body)

	@pytest.mark.parametrize("body, expected_code", [
		({"name": 'TEST_ADD_PHONE', "phone": "+79995554433"}, 200),
		({"name": 'Max'}, 400),
		({"phone": "+79995554433"}, 400),
		({"name": 'Max', "phone": "ABC123"}, 400),
	])
	def test_add_phone(self, body, expected_code):
		resp_code, resp_body = request(
			"post",
			host + '/add-phone',
			json_data=body
		)
		assert resp_code == expected_code
		if expected_code < 400:
			check_add_phone(body, resp_body)

	def test_delete_phone(self):
		phone_id = execute("SELECT id FROM phonebook WHERE name='TEST_USER'")[0][0]
		resp_code, resp_body = request(
			"delete",
			host + f'/remove-phone/{phone_id}'
		)
		check_remove_phone(resp_code, phone_id)
