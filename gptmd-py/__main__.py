# gptmd/__main__.py
import sys
from .intercept import fetch_convo
from .convert import convert_json_to_md

def main():
    if len(sys.argv) != 3:
        print("Usage: gptmd <chatgpt.com URL> <output-name>")
        sys.exit(1)

    url = sys.argv[1]
    name = sys.argv[2]
    json_file = f"{name}.json"
    md_file = f"{name}.md"

    fetch_convo(url, json_file)
    convert_json_to_md(json_file, md_file)

if __name__ == "__main__":
    main()

