import re

def clean_text(text):
    """Remove extra spaces and unwanted characters."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def validate_data(record, required_fields):
    """Ensure all required fields exist in the scraped record."""
    return all(record.get(field) for field in required_fields)
