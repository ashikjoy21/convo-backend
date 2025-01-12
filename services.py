import asyncio
from typing import Optional, Tuple
from groq import Groq
from TTS.api import TTS
from config import Config
from models import ChatRequest, ChatResponse
from database import Database

class ChatService:
    def __init__(self):
        self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
        self.db = Database()
        self.tts_model = None  # Initialize in setup_tts
    
    async def setup_tts(self):
        """Initialize TTS model."""
        if self.tts_model is None:
            self.tts_model = TTS(
                model_name="tts_models/en/ljspeech/vits",
                progress_bar=False
            )
    
    async def process_chat(
        self,
        request: ChatRequest
    ) -> Tuple[ChatResponse, bool]:
        """Process chat request and generate response."""
        try:
            # Get AI response
            response = await self.get_ai_response(request)
            
            # Generate audio
            audio_url = await self.generate_audio(response)
            
            # Save conversation
            await self.db.save_conversation(
                request.user_id,
                'user',
                request.message
            )
            await self.db.save_conversation(
                request.user_id,
                'assistant',
                response
            )
            
            return ChatResponse(
                text=response,
                audio_url=audio_url
            ), True
            
        except Exception as e:
            return ChatResponse(
                text="",
                error=str(e)
            ), False
    
    async def get_ai_response(self, request: ChatRequest) -> str:
        """Get response from AI model."""
        try:
            completion = await self.groq_client.chat.completions.create(
                messages=[
                    {"role": "user", "content": request.message}
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI response generation failed: {e}")
    
    async def generate_audio(self, text: str) -> Optional[str]:
        """Generate audio from text."""
        try:
            if self.tts_model is None:
                await self.setup_tts()
            
            # Implementation details for audio generation
            # This is a placeholder - implement actual audio generation logic
            return "audio_url_here"
        except Exception as e:
            raise Exception(f"Audio generation failed: {e}") 