"""Bundle index.html into a self-contained astermots.html with inline dictionary."""
import json, re, os

# --- Version management ---
VERSION_FILE = 'version.txt'
if os.path.exists(VERSION_FILE):
    with open(VERSION_FILE, 'r') as f:
        version = int(f.read().strip())
else:
    version = 0
version += 1
with open(VERSION_FILE, 'w') as f:
    f.write(str(version))
print(f'Version: v{version}')

with open('src/data/dictionary.json', 'r', encoding='utf-8') as f:
    dict_data = json.dumps(json.load(f), ensure_ascii=False, separators=(',', ':'))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Inject DICT_DATA before the main script
inject = f'<script>var DICT_DATA={dict_data};</script>\n'
html = html.replace('  <script>\n    let dictionary = [];', inject + '  <script>\n    let dictionary = [];', 1)

# Remove the external dictionary.js loader script block
ext_script = re.search(
    r'  <script>\s*// Load dictionary data via script tag.*?</script>',
    html, re.DOTALL
)
if ext_script:
    html = html[:ext_script.start()] + html[ext_script.end():]

# Stamp version
html = re.sub(r'>v\d+<', f'>v{version}<', html)

with open('astermots.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'astermots.html written ({len(html):,} chars)')
