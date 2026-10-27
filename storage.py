import json
import os

FILENAME = "expenses.json"
DATA_FILE = FILENAME  # Added for test suite compatibility alignment

def load_expenses():
    """Reads the JSON file and returns the saved expense list safely."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as file:
            json.dump([], file)
        return []
    
    try:
        with open(FILENAME, 'r') as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []

def save_expenses(expenses):
    """Writes the expense list to the JSON file persistently."""
    try:
        with open(FILENAME, 'w') as file:
            json.dump(expenses, file, indent=4)
        return True
    except IOError:
        return False
