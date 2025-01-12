import os
import sys
from pathlib import Path

# Add parent directory to path to import from project
sys.path.append(str(Path(__file__).parent.parent))

from database import Database
from dotenv import load_dotenv

load_dotenv()

async def init_database():
    """Initialize database tables and indexes."""
    db = Database()
    
    # SQL commands to create tables
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS api_keys (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            api_key VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP WITH TIME ZONE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            role VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_memory (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            type VARCHAR(50) NOT NULL,
            information TEXT NOT NULL,
            importance FLOAT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    try:
        for command in commands:
            await db.service_client.execute(command)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_database()) 