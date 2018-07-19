import pytest
from finTranslateBot.database.connection import DBConnection

@pytest.fixture()
def DB():
	return DBConnection()