from motor.motor_asyncio import AsyncIOMotorDatabase
from bson.objectid import ObjectId
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
import pytest_asyncio
import pytest

from services.mongo.conf import connect_to_mongodb, connect_to_test_mongodb
from services.rabbit import connect_to_rabbit
from main import app


@pytest.fixture
def test_client():
    global app
    app.dependency_overrides[connect_to_mongodb] = connect_to_test_mongodb
    app.dependency_overrides[connect_to_rabbit] = lambda: AsyncMock()
    client = TestClient(app)
    yield client
    client.close()

@pytest.fixture
def test_db():
    db = connect_to_test_mongodb()
    yield db
    
@pytest_asyncio.fixture(autouse=True)
async def clean_db(test_db: AsyncIOMotorDatabase):
    collections = await test_db.list_collection_names()
    for collection in collections:
        await test_db[collection].delete_many({})
    yield

@pytest_asyncio.fixture
async def compete_task_id(test_db: AsyncIOMotorDatabase):
    doc = {
            "status": "completed",
            "parameters": {
                "text": "python",
                "salary": None,
                "city": "Москва"
                },
            "jobs": [ObjectId("686a5d72a176b3a863b0ed4f")]
        }
    task_id = (await test_db["search_result"].insert_one(doc)).inserted_id
    yield task_id
    
@pytest_asyncio.fixture
async def process_task_id(test_db: AsyncIOMotorDatabase):
    doc = {
        "status": "processing",
        "parameters": {
            "text": "Java",
            "city": "Воронеж"
            },
        }
    task_id = (await test_db["search_result"].insert_one(doc)).inserted_id
    yield task_id