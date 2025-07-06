from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import pytest


@pytest.mark.asyncio
async def test_start_parsing(test_client: TestClient, test_db: AsyncIOMotorDatabase):
    request_data = {"text": "Python developer", "city": "Москва", "salary": 10_000}
    response = test_client.post("/parse", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "task_id" in data
    
    task = await test_db["search_result"].find_one({"_id": ObjectId(data["task_id"])})
    
    assert task is not None
    assert task["status"] == "processing"
    assert task["parameters"] == request_data
    
@pytest.mark.asyncio
async def test_start_parsing_invalid_data(test_client: TestClient):
    response = test_client.post("/parse", json={"city": "Москва"})
    
    assert response.status_code == 422
    assert "detail" in response.json()