import json
from datetime import datetime
import re

ROLE_ICONS = {
    "user": "🧑 User",
    "assistant": "🤖 Assistant",
    "system": "⚙️ System"
}

HEADING_PATTERN = re.compile(r"^(#+)(\s+)", re.MULTILINE)

def unix_to_utc(ts):
    if ts is None:
        return "(no timestamp)"
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M UTC")

def demote_headings(markdown_text, demote_by=3):
    def replacer(match):
        hashes, space = match.groups()
        return "#" * (len(hashes) + demote_by) + space
    return HEADING_PATTERN.sub(replacer, markdown_text)

def extract_conversation(data):
    mapping = data.get("mapping", {})
    root_id = next((k for k, v in mapping.items() if v.get("parent") is None), None)
    output_lines = []

    def walk(node_id):
        node = mapping.get(node_id)
        if not node:
            return
        message = node.get("message")
        if message:
            role = message.get("author", {}).get("role", "unknown")
            icon = ROLE_ICONS.get(role, role.capitalize())
            timestamp = message.get("create_time")
            timestamp_str = unix_to_utc(timestamp)

            parts = message.get("content", {}).get("parts", [])
            content = "\n\n".join(parts).strip()
            content = demote_headings(content)

            output_lines.append(f"## {icon} ({timestamp_str})\n\n{content}\n")

        for child_id in node.get("children", []):
            walk(child_id)

    walk(root_id)
    return "\n".join(output_lines)

def convert_json_to_md(input_file: str, output_file: str):
    with open(input_file, "r") as f:
        data = json.load(f)

    markdown_output = extract_conversation(data)

    with open(output_file, "w") as f:
        f.write(markdown_output)

    print(f"✅ Markdown exported to: {output_file}")

