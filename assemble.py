#!/usr/bin/env python3
"""Assemble lesson fragments into index.html."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).parent
INDEX = ROOT / "index.html"
FRAGMENTS = ROOT / "_fragments"
MARKER = "<!-- Further lessons will be inserted here -->"

fragment_files = [
    "block1rest.html",
    "block2.html",
    "block3.html",
    "block4.html",
    "block5.html",
    "block6.html",
    "block7.html",
    "block7rest.html",
]

html = INDEX.read_text(encoding="utf-8")

if MARKER not in html:
    print("ERROR: placeholder marker not found in index.html", file=sys.stderr)
    sys.exit(1)

blocks = []
missing = []
for name in fragment_files:
    p = FRAGMENTS / name
    if not p.exists():
        missing.append(name)
        continue
    blocks.append(p.read_text(encoding="utf-8").rstrip())

if missing:
    print(f"ERROR: missing fragments: {', '.join(missing)}", file=sys.stderr)
    sys.exit(1)

sections = "\n\n      ".join(blocks)
html = html.replace(MARKER, sections)
INDEX.write_text(html, encoding="utf-8")

ids = re.findall(r'<section class="lesson" id="(lesson-\d+)"', html)
print(f"OK: assembled {len(ids)} lessons into index.html")
for i in ids:
    print(f"  {i}")