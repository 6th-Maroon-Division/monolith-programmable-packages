import json
import os
import re
import sys
import urllib.request

ALLOWED = {"patch", "minor", "major"}
CHANGE_RE = re.compile(r"^\s*[-*]\s*(add|fix|tweak|remove):\s+\S", re.IGNORECASE)

def fail(msg):
    print("ERROR:", msg)
    sys.exit(1)

def gh_get(url, token):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        fail("GITHUB_EVENT_PATH is missing")

    token = os.environ.get("GITHUB_TOKEN", "")
    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    pr = event.get("pull_request")
    if not pr:
        fail("No pull_request payload")

    labels = {l["name"] for l in pr.get("labels", [])}
    selected = labels.intersection(ALLOWED)
    if len(selected) != 1:
        fail("Exactly one label is required: patch, minor, or major")

    body = pr.get("body") or ""
    if ":cl:" not in body:
        fail("PR body must contain :cl: block")

    lines = body.splitlines()
    cl_index = -1
    for i, line in enumerate(lines):
        if line.strip().lower() == ":cl:":
            cl_index = i
            break
    if cl_index < 0:
        fail("Missing :cl: header")

    valid_lines = 0
    for line in lines[cl_index + 1:]:
        if not line.strip():
            if valid_lines > 0:
                break
            continue
        if CHANGE_RE.match(line):
            valid_lines += 1
            continue
        if line.strip().startswith("#"):
            continue
        break

    if valid_lines == 0:
        fail("No valid changelog lines after :cl:")

    repo = os.environ.get("GITHUB_REPOSITORY")
    pr_number = pr.get("number")
    if not repo or not pr_number:
        fail("Missing repository or PR number")

    files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files?per_page=300"
    changed = gh_get(files_url, token)

    version_dirs = set()
    for item in changed:
        path = item.get("filename", "")
        parts = path.split("/")
        if len(parts) >= 4 and parts[0] == "packages":
            version_dirs.add("/".join(parts[:3]))

    required = ("lib.lua", "dependencies.txt", "meta.yml")
    for d in sorted(version_dirs):
        for name in required:
            p = os.path.join(d, name)
            if not os.path.exists(p):
                fail(f"Missing required file: {p}")

    print("PR validation passed")

if __name__ == "__main__":
    main()
