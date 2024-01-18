import string, secrets

def generate_random_string(length:int = 8):
    chars = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(chars) for _ in range(length))
    return random_string