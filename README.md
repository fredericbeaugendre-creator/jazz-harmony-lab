# Jazz Harmony Lab

A small Python tool to analyse jazz chord progressions.

## First goals

- Parse chord symbols such as Fmaj7, Gm7, C7, Dm7b5
- Read a chord grid from grid.txt
- Display chord tones
- Suggest scales or modes for each chord
- Find common tones between consecutive chords
- Detect simple jazz progressions such as II-V-I, secondary dominants, and tritone substitution candidates
- Generate a Markdown analysis report
- Help with composition and improvisation

## Supported chord symbols

maj7, m7, 7, m7b5, dim7, 6, m6, 9, m9, 13, 7b9, 7#9

## Example

Write a grid in `grid.txt`:

```text
| Dm7 G7 | Cmaj7 |
| Fmaj7 | Bm7b5 E7b9 | Am7 |
```

Run:

```bash
python3 main.py
```

The program writes `analysis.md` with:

- The original grid
- Parsed chords by bar
- Chord tones and suggested scales
- Detected harmonic movements
- Harmonic options for detected II-V-I movements

It also writes separate scale practice sheets in `practice_sheets/`, including:

- Scale notes and chord context
- Important target tones
- Common tones with nearby scales
- Simple resolution ideas
- Text guitar fretboard diagrams
- Piano notes and suggested right-hand fingering
