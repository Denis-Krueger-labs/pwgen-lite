import string

import pwgen

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