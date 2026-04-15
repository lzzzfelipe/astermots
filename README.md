# Frenchy 🇫🇷

A French language dictionary for elementary school kids featuring phonetic autocomplete — kids type what they *hear*, and Frenchy finds the word they mean.

## Why Phonetic Search?

French spelling is notoriously irregular. A child hearing "eau" might type "o", or hearing "pharmacie" might try "farmasie". Frenchy bridges that gap by matching words based on how they sound rather than how they're spelled, using French phonetic rules.

## Features

- **Phonetic autocomplete** — type a word the way it sounds and get real spelling suggestions
- **Kid-friendly definitions** — simple explanations written for ages 6–11
- **Visual cues** — illustrations and color-coded word categories (nouns, verbs, adjectives)
- **Audio pronunciation** — hear each word spoken aloud
- **Favorites** — save words to review later

## Tech Stack

- **React** with TypeScript
- **Vite** for builds
- **Tailwind CSS** for styling
- CSS animations for interactive feedback

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |
| `npm run test` | Run full test suite |
| `npm run test -- --run src/utils/phonetics.test.ts` | Run a single test file |

## Phonetic Engine

The core of Frenchy is a phonetic normalization engine that converts French text into a simplified sound representation. It handles:

- **Silent letters** — `temps` → `tã`, `heure` → `eur`
- **Vowel combinations** — `eau`/`au`/`o` all normalize to the same sound
- **Nasal vowels** — `an`/`en`, `in`/`ain`/`ein`, `on`/`om`
- **Consonant rules** — soft/hard `c` and `g`, silent final consonants, liaison markers

When a child types input, both the input and every dictionary entry are converted to their phonetic form, then matched using a prefix/fuzzy comparison.

## Project Structure

```
src/
├── components/       # React UI components
│   ├── SearchBar/    # Phonetic search input with autocomplete dropdown
│   ├── WordCard/     # Definition display with illustration and audio
│   └── Favorites/    # Saved words list
├── data/             # Dictionary data (words, definitions, categories)
├── hooks/            # Custom React hooks
├── utils/
│   └── phonetics.ts  # Phonetic normalization and matching engine
└── types/            # TypeScript type definitions
```

## Contributing

Contributions welcome — especially for expanding the dictionary dataset and improving phonetic rules. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
