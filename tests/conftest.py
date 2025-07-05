from fastapi.testclient import TestClient
from services.mongo.conf import connect_to_mongodb, connect_to_test_mongodb
import pytest

from main import app


@pytest.fixture
def test_client():
    app.dependency_overrides[connect_to_mongodb] = connect_to_test_mongodb
    client = TestClient(app)
    yield client
    client.close()
