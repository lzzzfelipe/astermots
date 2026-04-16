import csv
import json
import re
import unicodedata

# Load existing dictionary for definitions
with open('src/data/dictionary.json', 'r', encoding='utf-8-sig') as f:
    existing = json.load(f)

# Index existing entries by word
existing_by_word = {}
for e in existing:
    w = e['word'].lower()
    if w not in existing_by_word:
        existing_by_word[w] = e

# Extract words from CSV
words = []
with open('words_raw.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if not row or not row[0].strip().isdigit():
            continue
        freq = int(row[0].strip())
        lemme = row[1].strip()
        if lemme and freq <= 10000:
            words.append((freq, lemme))

print(f"Extracted {len(words)} words from CSV")

# Build new dictionary
new_dict = []
with_def = 0
without_def = 0

for freq, word in words:
    wl = word.lower()
    if wl in existing_by_word:
        entry = dict(existing_by_word[wl])
        entry['freq'] = freq
        new_dict.append(entry)
        with_def += 1
    else:
        entry = {
            'word': word,
            'freq': freq,
            'category': '',
            'definition': '',
            'example': ''
        }
        new_dict.append(entry)
        without_def += 1

print(f"With definitions: {with_def}")
print(f"Without definitions: {without_def}")
print(f"Total entries: {len(new_dict)}")

# Write output
with open('src/data/dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(new_dict, f, ensure_ascii=False, indent=2)

print("Written to src/data/dictionary.json")
