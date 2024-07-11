import asyncio
from unittest.mock import patch, MagicMock

from todo.main import Todo, app, consume, create_tables, get_data, get_item_by_id, add_item, update_item_id, delete_item_id, add_data_kafka
from todo.model import CreateItem, UpdateItem
from todo.database import engine


# Helper functions to mock database interactions
async def mock_get_data(session):
    return ["Mocked data"]

async def mock_get_item_by_id(item_id, session):
    return {"id": item_id, "name": "Mocked Item"}

async def mock_add_item(item, session):
    return {"id": 1, "name": item.name, "description": item.description}

async def mock_update_item_id(item_id, item_update, session):
    return {"id": item_id, "name": item_update.name, "description": item_update.description}

async def mock_delete_item_id(item_id, session):
    return True


class TestToDoApp:

    async def test_get_all_items(self):
        with patch.object(get_data, "get_data", mock_get_data):
            response = await app.test_client().get("/item")
            assert response.status_code == 200
            assert response.json() == ["Mocked data"]

    async def test_get_item_by_id(self):
        with patch.object(get_item_by_id, "get_item_by_id", mock_get_item_by_id):
            response = await app.test_client().get("/item/1")
            assert response.status_code == 200
            assert response.json() == {"id": 1, "name": "Mocked Item"}

    async def test_create_item(self):
        with patch.object(add_item, "add_item", mock_add_item):
            data = {"name": "New Item", "description": "This is a new item"}
            response = await app.test_client().post("/add_item", json=data)
            assert response.status_code == 200
            assert response.json() == {"id": 1, "name": data["name"], "description": data["description"]}

    async def test_update_item(self):
        with patch.object(update_item_id, "update_item_id", mock_update_item_id):
            data = {"name": "Updated Item"}
            response = await app.test_client().put("/update_item/1", json=data)
            assert response.status_code == 200
            assert response.json() == {"id": 1, **data}

    async def test_delete_item(self):
        with patch.object(delete_item_id, "delete_item_id", mock_delete_item_id):
            response = await app.test_
