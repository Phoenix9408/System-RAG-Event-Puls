import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    return {
        "mistral_api_key": os.getenv("MISTRAL_AI_KEY"),
        "embedding_model": "mistral-embed",
        "chat_model": "mistral-medium",
        "index_path": "culture_event_index",
        "memory_file": "conversation_memory.json",
        "default_region": "Île-de-France",
        "embedding_dim": 1024
    }
