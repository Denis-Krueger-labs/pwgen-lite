""" 
pwgen-lite
Minimalistic password generator in Python.

"""

import argparse
import secrets
import string
import hmac
import os
from hashlib import sha256

class HmacRng:

    """
    Educational HMAC-SHA256 based byte generator.
    Deterministic if the same seed is used.

    Not a full DRBG spec implementation; secrets-mode is recommended for real use. 
    """
    def __init__(self, key: bytes, context: bytes = b"pwgen-lite-hmac"):
        self.key = key
        self.context = context
        self.counter = 0
    
    def randbytes(self, n: int) -> bytes:
        out =bytearray()
        while len(out) < n:
            msg = self.counter.to_bytes(8, "big") + self.context
            block = hmac.new(self.key, msg, sha256).digest()
            out.extend(block)
            self.counter += 1
        return bytes(out[:n])

def bytes_to_password_hmac(length: int, alphabet: str, rng: HmacRng) -> str:
    """
    Convert HMAC-RNG bytes into password characters using rejcetion sampling to avoid modulo bias.
    """
    alph_len = len(alphabet)
    if alph_len < 2:
        raise ValueError("Alphabet too small.")
    
    #Largest multiple of alph_len less than 256 to avoid bias
    limit = (256 // alph_len) * alph_len

    chars = []
    while len(chars) < length:
        b = rng.randbytes(1)[0]
        if b >= limit:
            continue
        chars.append(alphabet[b % alph_len])
    
    return "".join(chars)

def build_alphabet(use_symbols: bool, exclude_ambiguous: bool) -> str:
    alphabet = BASE_ALPHABET + (SYMBOLS if use_symbols else "")
    if exclude_ambiguous:
        for ch in "O0Il1":
            alphabet = alphabet.replace(ch, "")
    return alphabet

# Base character sets
BASE_ALPHABET = string.ascii_letters + string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

def generate_password(length: int, use_symbols: bool, exclude_ambiguous: bool) -> str:
    """
    Generate a password of given length using secure randomness
    """

    alphabet = build_alphabet(use_symbols, exclude_ambiguous)
    return "".join(secrets.choice(alphabet) for _ in range(length))

def generate_password_hmac(length: int, use_symbols: bool, exclude_ambiguous: bool, seed: bytes) -> str:
    """
    Generate a password using the HMAC-based RNG for educational purposes.
    """
    alphabet = build_alphabet(use_symbols, exclude_ambiguous)
    rng = HmacRng(seed)
    return bytes_to_password_hmac(length, alphabet, rng)

def parse_arguments():
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(description="Generate a secure random password.")

    parser.add_argument("length", type=int, help="Length of the password (positive integer)")
    parser.add_argument("--symbols", action="store_true", help="Include symbols in the password")
    parser.add_argument("--exclude-ambigous", action="store_true", help="Exclude ambiguous characters (O,0,l,I,1)")
    parser.add_argument("--mode", choices=["secrets", "hmac"], default="secrets", help="RNG mode: secrets (recommended) or hmac (educational)")
    parser.add_argument("--seed-hex", default=None, help="(hmac mode) 32-byte seed as 64 hex characters. If omitted, a random seed is used.")
    return parser.parse_args()                    

def main():
    args = parse_arguments()

    if args.length <= 0:
        print("Error: Length must be a positive integer.")
        return
    if args.mode == "secrets":
        print(generate_password(args.length, args.symbols, args.exclude_ambiguous))
        return
    
    # HMAC mode
    if args.seed_hey is not None:
        try: 
            seed = bytes.fromhex(args.seed_hex)
        except ValueError:
            print("Invalid --seed-hex (must be hex).")
            return
        if len(seed) != 32:
            print("Invalid --seed-hex length (must be 64 hex chars for 32 bytes).")
            return
    else: 
        seed = os.urandom(32)
    
    print(generate_password_hmac(args.length, args.symbols, args.exclude_ambiguous, seed))
    
if __name__ == "__main__":
    main()