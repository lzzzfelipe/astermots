import re

with open('_test_script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Check brace balance
opens = js.count('{')
closes = js.count('}')
print(f'Braces: {{ = {opens}, }} = {closes}, diff = {opens - closes}')

opens = js.count('(')
closes = js.count(')')
print(f'Parens: ( = {opens}, ) = {closes}, diff = {opens - closes}')

opens = js.count('[')
closes = js.count(']')
print(f'Brackets: [ = {opens}, ] = {closes}, diff = {opens - closes}')

# Check AudioContext at top level (would fail if browser blocks it)
if 'const audioCtx = new' in js:
    idx = js.find('const audioCtx = new')
    print(f'\nAudioContext created at char {idx}')
    # Is it inside a function or at top level?
    before = js[:idx]
    depth = before.count('{') - before.count('}')
    print(f'  Brace depth at that point: {depth}')
    if depth <= 1:
        print('  WARNING: AudioContext at top-level scope - may throw if autoplay blocked')

# Check for template literal issues with backticks
backticks = js.count('`')
print(f'\nBackticks: {backticks} (should be even: {backticks % 2 == 0})')

# Find any 'const' or 'let' at depth 0 that reference DOM before DOMContentLoaded
print('\nChecking top-level DOM access...')
lines = js.split('\n')
for i, line in enumerate(lines):
    stripped = line.strip()
    if 'document.getElementById' in stripped or 'document.querySelector' in stripped:
        if 'function' not in stripped and 'innerHTML' not in stripped and '=>' not in stripped:
            if not stripped.startswith('//'):
                print(f'  Line {i+1}: {stripped[:100]}')
