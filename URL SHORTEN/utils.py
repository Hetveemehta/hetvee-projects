import random
import string

def generate_unique_code(db_reference, code_length=7):
    """Generates a unique, random short code."""
    characters = string.ascii_letters + string.digits
    
    # Try 10 times to find a unique code
    for _ in range(10):
        short_code = ''.join(random.choice(characters) for _ in range(code_length))
        if short_code not in db_reference:
            return short_code, code_length
    
    # If we fail, increase length (recursive retry)
    new_length = code_length + 1
    print(f"Warning: High collision rate. Increased code length to {new_length}.")
    return generate_unique_code(db_reference, new_length)