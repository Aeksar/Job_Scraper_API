from services.mongo.conf import  connect_to_test_mongodb
from bson import ObjectId
import pytest



@pytest.mark.asyncio
async def test_start_parsing(test_client):      
    response = test_client.post("/parse", json={"position": "Python developer", "city": "Москва"})
    assert response.status_code == 200
    
    data = response.json()
    print(data)
    assert "task_id" in data
    
    test_db = connect_to_test_mongodb()
    task = await test_db["search_result"].find_one({"_id": ObjectId(data["task_id"])})
    
    assert task is not None
    assert task["status"] == "processing"
    assert task["parameters"] == {"position": "Python developer", "city": "Москва", "salary": None}