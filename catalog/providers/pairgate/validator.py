from decimal import Decimal

def is_string_valid(text):
    if text and text.strip():
        return True
    return False


def is_positive_integer(value):
    return type(value) is int and value > 0


def is_positive_decimal(value):
    return type(value) in (float, Decimal) and value > 0


        
