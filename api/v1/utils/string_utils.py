from datetime import datetime
def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"

def parse_int(value: str):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def parse_float(value: str):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def parse_datetime(value: str):
    try:
        # Format: 'MM/DD/YYYY HH:MM:SS AM/PM' or similar
        return datetime.strptime(value, "%m/%d/%Y %I:%M:%S %p")
    except (ValueError, TypeError):
        return None