import os
import torch
import logging
from datetime import timedelta
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from quart import Quart, request, jsonify
from quart_cors import cors
from TTS.api import TTS
from groq import Groq
from supabase import create_client, Client
from dotenv import load_dotenv
from models import ChatRequest, ChatResponse
from services import ChatService
from utils import token_required, format_response

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not all([SUPABASE_URL, SUPABASE_API_KEY, GROQ_API_KEY]):
    raise EnvironmentError("Missing required environment variables")

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = timedelta(days=1)

# Initialize directories
output_dir = "temp_audio"
os.makedirs(output_dir, exist_ok=True)

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
service_client = create_client(
    SUPABASE_URL,
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

# Initialize application
app = Quart(__name__)
app = cors(app)
client = Groq(api_key=GROQ_API_KEY)

# Initialize thread pool
audio_thread_pool = ThreadPoolExecutor(max_workers=12)

# Initialize ChatService
chat_service = ChatService()

@lru_cache(maxsize=1000)
def get_cached_audio(text: str) -> str:
    return text

# Initialize TTS model
try:
    tts_model = TTS(
        model_name="tts_models/en/ljspeech/vits",
        progress_bar=False,
        gpu=torch.cuda.is_available()
    ).to('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Optimize model for inference
    tts_model.eval()
    torch.set_grad_enabled(False)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.enabled = True
        torch.backends.cudnn.deterministic = False
    
    # Warm up model
    logger.info("Warming up VITS model...")
    tts_model.tts("Warming up the model")
except Exception as e:
    logger.error(f"Failed to initialize VITS model: {e}")
    raise RuntimeError("Critical: VITS model initialization failed")

# Add your routes and handlers here
@app.route('/health', methods=['GET'])
async def health_check():
    return {'status': 'healthy'}, 200

# Chat endpoint
@app.route('/chat', methods=['POST'])
@token_required
async def chat(current_user):
    try:
        data = await request.get_json()
        
        if not data or 'message' not in data:
            return format_response({'error': 'Message is required'}, 400)
        
        chat_request = ChatRequest(
            message=data['message'],
            user_id=current_user,
            context=data.get('context')
        )
        
        response, success = await chat_service.process_chat(chat_request)
        
        if not success:
            return format_response({'error': response.error}, 500)
        
        return format_response({
            'text': response.text,
            'audio_url': response.audio_url
        })
    
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return format_response({'error': str(e)}, 500)

# Get conversation history
@app.route('/conversations', methods=['GET'])
@token_required
async def get_conversations(current_user):
    try:
        limit = request.args.get('limit', default=10, type=int)
        conversations = await chat_service.db.get_conversation_history(
            user_id=current_user,
            limit=limit
        )
        return format_response({'conversations': conversations})
    
    except Exception as e:
        logger.error(f"Get conversations error: {e}")
        return format_response({'error': str(e)}, 500)

# User memory endpoints
@app.route('/memory', methods=['POST'])
@token_required
async def save_memory(current_user):
    try:
        data = await request.get_json()
        
        if not all(k in data for k in ['type', 'information', 'importance']):
            return format_response({'error': 'Missing required fields'}, 400)
        
        success = await chat_service.db.save_user_memory(
            user_id=current_user,
            memory_type=data['type'],
            information=data['information'],
            importance=float(data['importance'])
        )
        
        if not success:
            return format_response({'error': 'Failed to save memory'}, 500)
        
        return format_response({'message': 'Memory saved successfully'})
    
    except Exception as e:
        logger.error(f"Save memory error: {e}")
        return format_response({'error': str(e)}, 500)

# Audio generation endpoint
@app.route('/generate-audio', methods=['POST'])
@token_required
async def generate_audio(current_user):
    try:
        data = await request.get_json()
        
        if not data or 'text' not in data:
            return format_response({'error': 'Text is required'}, 400)
        
        audio_url = await chat_service.generate_audio(data['text'])
        
        if not audio_url:
            return format_response({'error': 'Failed to generate audio'}, 500)
        
        return format_response({'audio_url': audio_url})
    
    except Exception as e:
        logger.error(f"Audio generation error: {e}")
        return format_response({'error': str(e)}, 500)

# User management endpoints
@app.route('/user', methods=['GET'])
@token_required
async def get_user_profile(current_user):
    try:
        user = await chat_service.db.get_user(current_user)
        
        if not user:
            return format_response({'error': 'User not found'}, 404)
        
        return format_response({'user': user})
    
    except Exception as e:
        logger.error(f"Get user profile error: {e}")
        return format_response({'error': str(e)}, 500)

# Error handlers
@app.errorhandler(404)
async def not_found(error):
    return format_response({'error': 'Not found'}, 404)

@app.errorhandler(500)
async def server_error(error):
    return format_response({'error': 'Internal server error'}, 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 