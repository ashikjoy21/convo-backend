import pytest
from services import ChatService
from models import ChatRequest, ChatResponse

@pytest.mark.asyncio
async def test_chat_service_initialization():
    service = ChatService()
    assert service is not None
    assert service.groq_client is not None
    assert service.db is not None

@pytest.mark.asyncio
async def test_process_chat():
    service = ChatService()
    request = ChatRequest(
        message="Hello, how are you?",
        user_id="test_user_id"
    )
    response, success = await service.process_chat(request)
    assert success
    assert isinstance(response, ChatResponse)
    assert response.text
    assert response.audio_url 