import jwt
import logging
from datetime import datetime, timedelta
from functools import wraps
from quart import request, jsonify
from config import Config

logger = logging.getLogger(__name__)

def generate_token(user_id: str) -> str:
    """Generate a JWT token for a user."""
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            Config.JWT_SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        logger.error(f"Token generation failed: {e}")
        raise

def token_required(f):
    """Decorator to check valid JWT token."""
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            current_user = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return await f(current_user, *args, **kwargs)
    
    return decorated

def validate_api_key(api_key: str) -> bool:
    """Validate API key against database."""
    # Implement API key validation logic here
    pass

def sanitize_input(text: str) -> str:
    """Sanitize user input."""
    # Implement input sanitization logic here
    return text.strip()

def format_response(data: dict, status: int = 200) -> tuple:
    """Format API response."""
    return {
        'status': 'success' if status < 400 else 'error',
        'data': data
    }, status 