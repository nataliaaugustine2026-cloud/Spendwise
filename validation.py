import math
from datetime import datetime

VALID_CATEGORIES = ["Food", "Travel", "Education", "Utilities", "Entertainment", "Other"]

def is_valid_amount(amount_str):
    """Checks if the amount string represents a positive, finite number."""
    try:
        amount = float(amount_str)
        return math.isfinite(amount) and amount > 0
    except (ValueError, TypeError):
        return False

def validate_expense_data(description, amount_str, category, date_str):
    """
    Validates form data from the user interface.
    Returns: (is_valid, error_message, cleaned_amount)
    """
    if not description or not description.strip():
        return False, "Description cannot be left blank.", 0

    # Utilises the required is_valid_amount helper function internally
    if not is_valid_amount(amount_str):
        return False, "Amount must be a valid positive number format (Infinity/NaN blocked).", 0
        
    amount = float(amount_str)

    if category not in VALID_CATEGORIES:
        return False, f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}", 0

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return False, "Date must follow the format YYYY-MM-DD.", 0

    return True, None, amount
