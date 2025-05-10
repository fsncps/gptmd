import sys
import json
import requests
from pathlib import Path

# Always resolve relative to the script location
SCRIPT_DIR = Path(__file__).resolve().parent
TOKEN_FILE = SCRIPT_DIR / "token.txt"
BASE_URL = "https://chatgpt.com"

def read_token():
    return TOKEN_FILE.read_text().strip()

def fetch_bearer(session, cookies):
    print("🔑 Fetching Bearer token via /api/auth/session...")
    r = session.get(
        f"{BASE_URL}/api/auth/session",
        cookies=cookies,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "application/json",
            "Referer": BASE_URL,
            "Accept-Language": "en-US,en;q=0.9"
        }
    )
    r.raise_for_status()
    access_token = r.json().get("accessToken")
    if not access_token:
        raise RuntimeError("❌ Could not retrieve Bearer token (accessToken missing).")
    print("✅ Bearer token acquired.")
    return access_token

def fetch_convo(convo_url: str, output_file: str):
    convo_id = convo_url.rstrip("/").split("/")[-1]
    api_url = f"{BASE_URL}/backend-api/conversation/{convo_id}"

    token = read_token()
    cookies = {"__Secure-next-auth.session-token": token}
    session = requests.Session()

    bearer_token = fetch_bearer(session, cookies)

    print(f"🌐 Fetching conversation {convo_id} directly from backend API...")
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Referer": BASE_URL,
        "Accept-Language": "en-US,en;q=0.9"
    }

    r = session.get(api_url, headers=headers, cookies=cookies)
    r.raise_for_status()
    convo_json = r.json()

    with open(output_file, "w") as f:
        json.dump(convo_json, f, indent=2)
    print(f"✅ Conversation JSON saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python intercept.py <chatgpt.com URL> <output-name>")
        sys.exit(1)
    url = sys.argv[1]
    outname = sys.argv[2]
    fetch_convo(url, f"{outname}.json")

