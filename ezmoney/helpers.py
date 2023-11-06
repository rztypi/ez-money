import re
from datetime import date


def validate_amount(amount):
    pattern = r"(?:^\d+(?:\.\d{0,2})?$)|(?:^\d*\.\d{1,2}?$)"
    if re.match(pattern, amount) is None:
        return False
    
    try:
        float_amount = float(amount)
    except ValueError:
        return False
    
    if float_amount == 0:
        return False
    
    return True


def validate_description(description):
    return description.strip() != ""


def validate_date(_date):
    try:
        date.fromisoformat(_date)
    except ValueError:
        return False
        
    return True


def currency(value):
    return f"₱{value:,.2f}"