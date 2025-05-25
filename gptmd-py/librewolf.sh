#!/usr/bin/env bash
set -euo pipefail

# Step 1: Locate default profile from ~/.librewolf/profiles.ini
PROFILE_INI="$HOME/.librewolf/profiles.ini"
DEFAULT_PATH=$(awk -F= '/^Path=/ {path=$2} /^Default=1/ {print path}' "$PROFILE_INI")

if [[ -z "$DEFAULT_PATH" ]]; then
   echo "No default profile found in $PROFILE_INI" >&2
   exit 1
fi

PROFILE_DIR="$HOME/.librewolf/$DEFAULT_PATH"
SQLITE="$PROFILE_DIR/cookies.sqlite"

if [[ ! -f "$SQLITE" ]]; then
   echo "cookies.sqlite not found at $SQLITE" >&2
   exit 1
fi

# Step 2: Copy to /tmp to avoid locked DB issues
TMP_DB="/tmp/librewolf_cookies.sqlite"
cp "$SQLITE" "$TMP_DB"

# Step 3: Extract session token (adjust domain and cookie name as needed)
# This targets cookies used by ChatGPT, for example
sqlite3 "$TMP_DB" <<'EOF'
.headers on
.mode column
SELECT name, value, host
FROM moz_cookies
WHERE name LIKE '%session%' OR name LIKE '%token%' COLLATE NOCASE;
EOF

# Optional: Extract specific token (ChatGPT-style example)
# TOKEN=$(sqlite3 "$TMP_DB" "SELECT value FROM moz_cookies WHERE name = '__Secure-next-auth.session-token';")
# echo "Session Token: $TOKEN"

# Clean up if needed
# rm "$TMP_DB"
