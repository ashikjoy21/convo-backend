import pytest
from database import Database

@pytest.mark.asyncio
async def test_database_connection():
    db = Database()
    assert db.client is not None
    assert db.service_client is not None

@pytest.mark.asyncio
async def test_save_conversation():
    db = Database()
    success = await db.save_conversation(
        user_id="test_user",
        role="user",
        content="Test message"
    )
    assert success 