import pytest
from .utils import execute


@pytest.fixture(scope="class")
def phonebook_fixture():
	execute(f"INSERT INTO phonebook(name, phone) VALUES('TEST_USER', '+79998887766')", get_id=True)
	yield
	execute(f"DELETE FROM phonebook")
