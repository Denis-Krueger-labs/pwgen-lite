# pwgen-lite

Minimal password generator written in Python.

## Features

- Cryptographically secure randomness via `secrets`
- Optional HMAC-SHA256 deterministic RNG mode (educational)
- Optional symbol inclusion
- Optional exclusion of ambiguous characters (`O 0 I l 1`)
- Multiple password generation (`--count`)
- Brute-force strength estimate (entropy + time model)
- Clean CLI interface
- Test suite with pytest

## Usage

Generate a 16-character password:
```bash
python pwgen.py 16
```

Generate a 16-character password including symbols:
```bash
python pwgen.py 16 --symbols
```

Generate 5 passwords including symbols:
```bash
python pwgen.py 16 --symbols --count 5
```

Use HMAC mode with fixed seed (deterministic output):
```bash
python3 pwgen.py 16 --mode hmac --seed-hex <64-hex-chars>
```

Disable strength output:
```bash
python3 pwgen.py 16 --no-strength
```

Show help
```bash
python pwgen.py --help
```

## Password Strength Model
Let:
- `A` = alphabet size
- `L` = password length
Search space:
```
A^L
```

Entropy (bits):
```
L * log2(A)
```

Average brute-force time:
```
0.5 * A^L / R
```

Where `R` = guesses per second.

## Built-in Scenarios 
| Scenario | Guess Rate | 
|---------------|---------------|
| online| 10/s | 
| offline-fast | 1e10/s | 
| offline-very-fast | 1e11/s | 

## Override manually
```bash
python3 pwgen.py 16 --rate 5e9
```
> Strength estimate assumes uniformly random passwords and brute-force 
> only. Real cracking speed depends heavily on hash algorithm and attack > conditions.


## Design Principles
- Secure by default
- Avoid predictable randomness (random is not used)
- Avoid modulo bias
- Clear separation of concerns
- Deterministic testing support
- Clean and readable implementation
- Built incrementally with structured commit history

## Testing

Install pytest:

```bash
python -m pip install pytest
```
Run tests:
```bash
pytest
```
---

## Ensure imports work
For the tests to import `pwgen`, run pytest from the repo root:

```bash
pytest
```
If it complains it can’t find `pwgen`, run:
```bash 
python -m pytest
```

## RNG Modes

**secrets (default)**
 uses Python's `secrets` module 
 recommended for real-world use.
**hmac (educational)** 
HMAC-SHA256 based deterministic generator.
- Same seed → same password sequence
- Demonstrates counter-based deterministic random byte generation
- Includes rejection sampling to avoid modulo bias

Examples:

```bash
python3 pwgen.py 16
python3 pwgen.py 16 --symbols
python3 pwgen.py 16 --mode hmac
python3 pwgen.py 16 --mode hmac --seed-hex <64-hex-chars>
```


## Goals

- Use secure randomness by default
- Provide an educational hash-based RNG mode
- Keep implementation clean and readable
- Avoid common randomness mistakes (e.g., modulo bias)

This project is built incrementally with clear commit history.

