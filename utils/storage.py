import json
import os
from models.user import User

DATABASE = "data/database.json"

def load_data():
    """
    Loads the database file. Returns a dict structure.
    Guarantees key presence and auto-heals corrupted JSON.
    """
    default_structure = {"users": [], "projects": [], "tasks": []}
    
    if not os.path.exists(DATABASE):
        return default_structure

    try:
        with open(DATABASE, "r") as file:
            data = json.load(file)
            # Ensure all keys exist
            for key in default_structure:
                if key not in data:
                    data[key] = []
            
            # Sync ID counter so new instances don't clash
            if data["users"]:
                max_id = max(u["id"] for u in data["users"])
                User.id_counter = max_id + 1
                
            return data
    except (json.JSONDecodeError, TypeError):
        return default_structure

def save_data(data):
    """
    Persists data dictionary cleanly to database.json.
    """
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    with open(DATABASE, "w") as file:
        json.dump(data, file, indent=4)