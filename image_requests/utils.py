from datetime import datetime

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False
    
def is_end_after_start(start_date_str, end_date_str):
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        end = datetime.strptime(end_date_str, "%Y-%m-%d")
        return end > start
    except ValueError:
        return False
    
def is_integer(value):
    try:
        int(value)     
        return True
    except (ValueError, TypeError):
        return False