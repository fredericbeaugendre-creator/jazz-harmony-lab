# Jazz Harmony Lab

A small Python tool to analyse jazz chord progressions.

## First goals

- Parse chord symbols such as Fmaj7, Gm7, C7, Dm7b5
- Read a chord grid from grid.txt
- Display chord tones
- Suggest scales or modes for each chord
- Find common tones between consecutive chords
- Detect simple jazz progressions such as II-V-I
- Help with composition and improvisation

## Supported chord symbols

maj7, m7, 7, m7b5, dim7, 6, m6, 9, m9, 13, 7b9, 7#9

## Example

Write a grid in `grid.txt`:

| Fmaj7 | D7b9 | Gm9 C13 | F6 |
| Bm7b5 E7#9 | Am6 | Cdim7 |

Run:

```bash
python3 main.py
```

Output:

Fmaj7 -> F A C E  
D7b9 -> D Gb A C Eb  
Gm9 -> G Bb D F A  

Suggested scales:

Fmaj7 -> F Ionian, F Lydian  
D7b9 -> D half-whole diminished, D altered, D phrygian dominant  

Common tones:

Fmaj7 to Gm7: F  
Gm7 to C7: G, Bb  
C7 to Fmaj7: C, E
