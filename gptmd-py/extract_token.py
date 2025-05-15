import os
import sqlite3
import configparser
from pathlib import Path
import shutil
import sys

def find_default_profile(profiles_ini_path: Path) -> Path:
    config = configparser.ConfigParser()
    config.read(profiles_ini_path)
    for section in config.sections():
        if config.has_option(section, "Default") and config.get(section, "Default") == "1":
            return Path(config.get(section, "Path"))
    raise RuntimeError("Default profile not found in profiles.ini")

def copy_sqlite_db(profile_dir: Path) -> Path:
    src = profile_dir / "cookies.sqlite"
    if not src.exists():
        raise FileNotFoundError(f"cookies.sqlite not found at {src}")
    dst = Path("/tmp/librewolf_cookies.sqlite")
    shutil.copy2(src, dst)
    return dst

def extract_tokens(db_path: Path) -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
        SELECT name, value FROM moz_cookies
        WHERE host = '.chatgpt.com'
          AND name IN ('__Secure-next-auth.session-token.0', '__Secure-next-auth.session-token.1')
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    tokens = {name: value for name, value in rows}
    try:
        return tokens['__Secure-next-auth.session-token.0'] + tokens['__Secure-next-auth.session-token.1']
    except KeyError as e:
        raise RuntimeError(f"Missing token part: {e}")

def main():
    # Locate profile
    home = Path.home()
    profiles_ini = home / ".librewolf" / "profiles.ini"
    profile_path = find_default_profile(profiles_ini)
    full_profile_path = home / ".librewolf" / profile_path

    # Copy DB and extract token
    db_copy = copy_sqlite_db(full_profile_path)
    combined_token = extract_tokens(db_copy)

    # Save to token.txt in same dir as script
    script_dir = Path(__file__).resolve().parent
    output_file = script_dir / "token.txt"
    with open(output_file, "w") as f:
        f.write(combined_token)

    print(f"Token written to {output_file}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

