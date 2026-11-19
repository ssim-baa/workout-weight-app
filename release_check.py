# Pre-push check for the app (stdlib only). Run: D:\Python313\python.exe -s release_check.py
# Fails if the three version markers disagree or if obvious leftovers are present.
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


html, sw = read("index.html"), read("sw.js")
v_html = re.search(r"const APP_VERSION = '([^']+)'", html).group(1)
v_json = json.loads(read("version.json"))["version"]
v_sw = re.search(r"const CACHE = 'workout-v([^']+)'", sw).group(1)
problems = []
if not (v_html == v_json == v_sw):
    problems.append(f"version mismatch: index.html {v_html}, version.json {v_json}, sw.js {v_sw}")
for pat in ("github_pat_", "ghp_"):
    for name in ("index.html", "sw.js", "manifest.webmanifest", "version.json"):
        if pat in read(name).replace('placeholder="github_pat_...', ""):
            problems.append(f"token-like string '{pat}' in {name}")
# every onclick handler must be defined somewhere in the script
handlers = set(re.findall(r'onclick="([A-Za-z_]\w*)\(', html))
for h in sorted(handlers):
    if not re.search(rf"(function\s+{h}\s*\(|window\.{h}\s*=)", html):
        problems.append(f"onclick handler not defined: {h}")
# every getElementById target must exist as an id
ids = set(re.findall(r'id="([^"]+)"', html))
for t in sorted(set(re.findall(r"getElementById\('([^'$]+)'\)", html))):
    if t not in ids:
        problems.append(f"getElementById target missing: {t}")
print(f"version {v_html}; handlers {len(handlers)}; ids {len(ids)}")
if problems:
    print("\n".join("FAIL " + p for p in problems))
    sys.exit(1)
print("OK")
