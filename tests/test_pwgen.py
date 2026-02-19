import string
import pwgen
import subprocess
import sys

def test_length_without_symbols():
   pw = pwgen.generate_password(32, use_symbols=False, exclude_ambiguous=False)
   assert len(pw) == 32

def test_length_with_symbols():
   pw = pwgen.generate_password(48, use_symbols=True, exclude_ambiguous=False)
   assert len(pw) == 48

def test_characters_without_symbols():
   allowed = set(string.ascii_letters + string.digits)
   pw = pwgen.generate_password(128, use_symbols=False, exclude_ambiguous=False)
   assert set(pw).issubset(allowed)

def test_charset_with_symbols():
    allowed = set(string.ascii_letters + string.digits + pwgen.SYMBOLS)
    pw = pwgen.generate_password(128, use_symbols=True, exclude_ambiguous=False)
    assert set(pw).issubset(allowed)

def test_exclude_ambiguous():
    pw = pwgen.generate_password(256, use_symbols=False, exclude_ambiguous=True)
    for ch in "O0Il1":
        assert ch not in pw

def test_hmac_mode_deterministic_with_seed():
   seed = bytes.fromhex("00" * 32)
   pw1=pwgen.generate_password_hmac(64, use_symbols=False, exclude_ambiguous=False, seed=seed)
   pw2=pwgen.generate_password_hmac(64, use_symbols=False, exclude_ambiguous=False, seed=seed)
   assert pw1 == pw2

def test_hmac_mode_respects_charset():
   seed = bytes.fromhex("11" * 32)
   pw = pwgen.generate_password_hmac(128, use_symbols=True, exclude_ambiguous=True, seed=seed)
   allowed = set(string.ascii_letters + string.digits + pwgen.SYMBOLS)
   for ch in "O0Il1":
      allowed.discard(ch)
   assert set(pw).issubset(allowed)

def test_count_outputs_correct_number_of_lines():
   result = subprocess.run([sys.executable, "pwgen.py", "8", "--count", "3", "--no-strength"], capture_output=True, text=True, check=True)
   
   # split output into lines and remove empty lines
   lines = [line for line in result.stdout.splitlines() if line.strip()]

   assert len(lines) == 3
   assert all(len(line) == 8 for line in lines)

def test_count_must_be_positive():
   result = subprocess.run([sys.executable, "pwgen.py", "8", "--count", "0"], capture_output=True, text=True)
   assert result.returncode != 0

def test_count_cli_lines():
   result = subprocess.run([sys.executable, "pwgen.py", "6", "--count", "4", "--no-strength"], capture_output=True, text=True, check=True)
   lines = [line for line in result.stdout.splitlines() if line.strip()]
   assert len(lines) == 4
   assert all(len(line) == 6 for line in lines) 

def test_hmac_count_not_all_equal():
    seed = "11" * 32
    res = subprocess.run([sys.executable, "pwgen.py", "10", "--mode", "hmac", "--count", "5", "--no-strength", "--seed-hex", seed], capture_output=True, text=True, check=True)
    lines = [ln for ln in res.stdout.splitlines() if ln.strip()]
    assert len(lines) == 5
    assert len(set(lines)) == 5  # should all be different