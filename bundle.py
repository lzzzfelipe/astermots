"""Bundle index.html into a self-contained astermots.html with inline dictionary."""
import json, re

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

with open('astermots.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'astermots.html written ({len(html):,} chars)')
