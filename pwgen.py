""" 
pwgen-lite
Minimalistic password generator in Python.

"""
import secrets
import string

# Base character sets
BASE_ALPHABET = string.ascii_letters + string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

def generate_password(length: int, use_symbols: bool) -> str:
    """
    Generate a password of given length using secure randomness
    """
    
    alphabet = BASE_ALPHABET

    if use_symbols:
        alphabet += SYMBOLS

    return "".join(secrets.choice(alphabet) for _ in range(length))


def main():
    raw = input("Enter password length: ").strip()

    if not raw.isdigit():
        print("Invalid input. Please enter a valid positive number. ")
        return
    
    length = int(raw)

    if length <= 0:
        print("Length must be greater then 0.")
        return 
    
    symbol_choice = input("Include symbols? (y/n):").strip().lower()
    use_symbols = symbol_choice == 'y'


    password = generate_password(length, use_symbols)
    print("Generated password:", password)

    
if __name__ == "__main__":
    main()