# pwgen-lite

Minimal password generator written in Python.

## Features

- Secure randomness using Python's `secrets` module
- Optional symbol support
- Clean command-line interface using `argparse`

## Usage

Generate a 16-character password:

```bash
python pwgen.py 16
```
Generate a 16-character password including symbols:
```bash
python pwgen.py 16 --symbols
```

Show help
```bash
python pwgen.py --help
```
## Design Principles
- Secure by default
- Avoid predictable randomness (random is not used)
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

## 4) Ensure imports work
For the tests to import `pwgen`, run pytest from the repo root:

```bash
pytest
```
If it complains it can’t find `pwgen`, run:
```bash 
python -m pytest
```

## RNG Modes

- **secrets (default)**: uses Python's `secrets` module (recommended for real passwords)
- **hmac**: educational HMAC-SHA256 based generator (deterministic when a seed is provided)

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

