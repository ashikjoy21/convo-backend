from typing import Dict, List, Optional
from supabase import create_client, Client
from config import Config

class Database:
    def __init__(self):
        self.client: Client = create_client(
            Config.SUPABASE_URL,
            Config.SUPABASE_API_KEY
        )
        self.service_client: Client = create_client(
            Config.SUPABASE_URL,
            Config.SUPABASE_SERVICE_ROLE_KEY
        )
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Retrieve user information."""
        try:
            response = self.client.table('users')\
                .select('*')\
                .eq('id', user_id)\
                .single()\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    async def save_conversation(
        self,
        user_id: str,
        role: str,
        content: str
    ) -> bool:
        """Save conversation to database."""
        try:
            self.client.table('conversations').insert({
                'user_id': user_id,
                'role': role,
                'content': content
            }).execute()
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    async def get_conversation_history(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """Retrieve conversation history."""
        try:
            response = self.client.table('conversations')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('timestamp', desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    async def save_user_memory(
        self,
        user_id: str,
        memory_type: str,
        information: str,
        importance: float
    ) -> bool:
        """Save user memory to database."""
        try:
            self.client.table('user_memory').insert({
                'user_id': user_id,
                'type': memory_type,
                'information': information,
                'importance': importance
            }).execute()
            return True
        except Exception as e:
            print(f"Error saving user memory: {e}")
            return False 