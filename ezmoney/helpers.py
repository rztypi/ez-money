from datetime import date

from currencies import Currency


def validate_amount(amount):
    if "." in amount and len(amount.split(".")[-1]) > 2:
        return False
    
    try:
        float_amount = float(amount)
    except ValueError:
        return False
    
    if float_amount < -1_000_000_000 or float_amount > 1_000_000_000:
        return False
    
    return True


def validate_description(description):
    return description.strip() != ""


def validate_date(_date):
    try:
        date_obj = date.fromisoformat(_date)
    except ValueError:
        return False
    
    if date_obj > date.today():
        return False
        
    return True


def currency(number, with_sign=False):
    sign = ""
    if with_sign:
        if number > 0:
            sign = "+ "
        elif number < 0:
            sign = "- "

    formatted_number = f"{abs(number):,.2f}"
    return f"{sign}{Currency('PHP').get_money_format(formatted_number)}"


def text_color(number):
    if number > 0:
        return "text-success"
    elif number < 0:
        return "text-danger"
    else:
        return ""