from fastapi.testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_get_task_status_processing(test_client: TestClient, process_task_id):
    response = test_client.get(f"/task/{process_task_id}")
    
    assert response.status_code == 200
    assert response.json() == {
        "status": "processing",
        "message": "wait bro"
    }


@pytest.mark.asyncio
async def test_get_task_status_completed(test_client: TestClient, compete_task_id):
    response = test_client.get(f"/task/{compete_task_id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data["status"] == "completed"
    assert "result" in data
    

@pytest.mark.asyncio
async def test_get_nonexistent_task(test_client: TestClient):
    response = test_client.get("/task/random_task_id")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found task"}