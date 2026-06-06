# Jazz Harmony Analysis

## 1. Original grid

```text
| Dm7 G7 | Cmaj7 |
| Fmaj7 | Bm7b5 E7b9 | Am7 |
```

## 2. Parsed chords by bar

- Bar 1: Dm7, G7
- Bar 2: Cmaj7
- Bar 3: Fmaj7
- Bar 4: Bm7b5, E7b9
- Bar 5: Am7

## 3. Chord tones for each chord

- **Dm7**
  - Function: minor seventh color
  - Chord tones: D, F, A, C
  - Suggested scales: D Dorian, D Aeolian
  - Important tones: 3rd: F, 7th: C
- **G7**
  - Function: dominant
  - Chord tones: G, B, D, F
  - Suggested scales: G Mixolydian, G Lydian dominant
  - Important tones: 3rd: B, 7th: F
- **Cmaj7**
  - Function: major tonic color
  - Chord tones: C, E, G, B
  - Suggested scales: C Ionian, C Lydian
  - Important tones: 3rd: E, 7th: B
- **Fmaj7**
  - Function: major tonic color
  - Chord tones: F, A, C, E
  - Suggested scales: F Ionian, F Lydian
  - Important tones: 3rd: A, 7th: E
- **Bm7b5**
  - Function: half-diminished pre-dominant
  - Chord tones: B, D, F, A
  - Suggested scales: B Locrian, B Locrian natural 2
  - Important tones: 3rd: D, 7th: A
- **E7b9**
  - Function: dominant
  - Chord tones: E, Ab, B, D, F
  - Suggested scales: E half-whole diminished, E altered, E phrygian dominant
  - Important tones: 3rd: Ab, 7th: D, b9: F
- **Am7**
  - Function: minor seventh color
  - Chord tones: A, C, E, G
  - Suggested scales: A Dorian, A Aeolian
  - Important tones: 3rd: C, 7th: G

## 4. Detected harmonic movements

- II-V-I major: Dm7 -> G7 -> Cmaj7 in C
- II-V-I minor: Bm7b5 -> E7b9 -> Am7 in A
- secondary dominant: G7 -> Cmaj7 resolving to Cmaj7
- secondary dominant: E7b9 -> Am7 resolving to Am7
- tritone substitution candidate: G7: try Db7
- tritone substitution candidate: E7b9: try Bb7

## 5. Harmonic options for detected II-V-I movements

### II-V-I major in C: Dm7 -> G7 -> Cmaj7

### Inside / diatonic option

- **Dm7**
  - Function: II in major
  - Chord tones: D, F, A, C
  - Suggested scale: D Dorian
  - Important tones: 3rd: F, 7th: C
- **G7**
  - Function: V in major
  - Chord tones: G, B, D, F
  - Suggested scale: G Mixolydian
  - Important tones: 3rd: B, 7th: F
- **Cmaj7**
  - Function: I in major
  - Chord tones: C, E, G, B
  - Suggested scale: C Ionian
  - Important tones: 3rd: E, 7th: B

Common chord tones:
- Dm7 to G7: D, F
- G7 to Cmaj7: G, B

Common scale tones:
- D Dorian to G Mixolydian: D, E, F, G, A, B, C
- G Mixolydian to C Ionian: G, A, B, C, D, E, F

Resolution idea: Keep guide tones clear: the dominant 7th resolves down, and the dominant 3rd resolves toward the tonic.

### Altered dominant option

- **Dm7**
  - Function: II in major
  - Chord tones: D, F, A, C
  - Suggested scale: D Dorian
  - Important tones: 3rd: F, 7th: C
- **G7#9**
  - Function: V in major
  - Chord tones: G, B, D, F, Bb
  - Suggested scale: G altered
  - Important tones: 3rd: B, 7th: F, #9: Bb
- **Cmaj7**
  - Function: I in major
  - Chord tones: C, E, G, B
  - Suggested scale: C Ionian
  - Important tones: 3rd: E, 7th: B

Common chord tones:
- Dm7 to G7#9: D, F
- G7#9 to Cmaj7: G, B

Common scale tones:
- D Dorian to G altered: F, G, B
- G altered to C Ionian: G, B, F

Resolution idea: Resolve #9/b9 colors by half step into stable chord tones on the tonic.

### Half-whole diminished dominant option

- **Dm7**
  - Function: II in major
  - Chord tones: D, F, A, C
  - Suggested scale: D Dorian
  - Important tones: 3rd: F, 7th: C
- **G7b9**
  - Function: V in major
  - Chord tones: G, B, D, F, Ab
  - Suggested scale: G half-whole diminished
  - Important tones: 3rd: B, 7th: F, b9: Ab
- **Cmaj7**
  - Function: I in major
  - Chord tones: C, E, G, B
  - Suggested scale: C Ionian
  - Important tones: 3rd: E, 7th: B

Common chord tones:
- Dm7 to G7b9: D, F
- G7b9 to Cmaj7: G, B

Common scale tones:
- D Dorian to G half-whole diminished: D, E, F, G, B
- G half-whole diminished to C Ionian: G, B, D, E, F

Resolution idea: Use b9 and diminished passing tones as tension, then land on tonic chord tones.

### Tritone substitution option

- **Dm7**
  - Function: II in major
  - Chord tones: D, F, A, C
  - Suggested scale: D Dorian
  - Important tones: 3rd: F, 7th: C
- **Db7**
  - Function: dominant
  - Chord tones: Db, F, Ab, B
  - Suggested scale: Db Lydian dominant
  - Important tones: 3rd: F, 7th: B
- **Cmaj7**
  - Function: I in major
  - Chord tones: C, E, G, B
  - Suggested scale: C Ionian
  - Important tones: 3rd: E, 7th: B

Common chord tones:
- Dm7 to Db7: F
- Db7 to Cmaj7: B

Common scale tones:
- D Dorian to Db Lydian dominant: F, G, B
- Db Lydian dominant to C Ionian: F, G, B

Resolution idea: Move the substitute dominant by half step into the tonic root or 5th.

### II-V-I minor in A: Bm7b5 -> E7b9 -> Am7

### Inside / diatonic option

- **Bm7b5**
  - Function: II in minor
  - Chord tones: B, D, F, A
  - Suggested scale: B Locrian
  - Important tones: 3rd: D, 7th: A
- **E7b9**
  - Function: V in minor
  - Chord tones: E, Ab, B, D, F
  - Suggested scale: E phrygian dominant
  - Important tones: 3rd: Ab, 7th: D, b9: F
- **Am7**
  - Function: I in minor
  - Chord tones: A, C, E, G
  - Suggested scale: A Dorian
  - Important tones: 3rd: C, 7th: G

Common chord tones:
- Bm7b5 to E7b9: B, D, F
- E7b9 to Am7: E

Common scale tones:
- B Locrian to E phrygian dominant: B, C, D, E, F, A
- E phrygian dominant to A Dorian: E, A, B, C, D

Resolution idea: Keep guide tones clear: the dominant 7th resolves down, and the dominant 3rd resolves toward the tonic.

### Altered dominant option

- **Bm7b5**
  - Function: II in minor
  - Chord tones: B, D, F, A
  - Suggested scale: B Locrian
  - Important tones: 3rd: D, 7th: A
- **E7#9**
  - Function: V in minor
  - Chord tones: E, Ab, B, D, G
  - Suggested scale: E altered
  - Important tones: 3rd: Ab, 7th: D, #9: G
- **Am7**
  - Function: I in minor
  - Chord tones: A, C, E, G
  - Suggested scale: A Dorian
  - Important tones: 3rd: C, 7th: G

Common chord tones:
- Bm7b5 to E7#9: B, D
- E7#9 to Am7: E, G

Common scale tones:
- B Locrian to E altered: C, D, E, F, G
- E altered to A Dorian: E, G, C, D

Resolution idea: Resolve #9/b9 colors by half step into stable chord tones on the tonic.

### Half-whole diminished dominant option

- **Bm7b5**
  - Function: II in minor
  - Chord tones: B, D, F, A
  - Suggested scale: B Locrian
  - Important tones: 3rd: D, 7th: A
- **E7b9**
  - Function: V in minor
  - Chord tones: E, Ab, B, D, F
  - Suggested scale: E half-whole diminished
  - Important tones: 3rd: Ab, 7th: D, b9: F
- **Am7**
  - Function: I in minor
  - Chord tones: A, C, E, G
  - Suggested scale: A Dorian
  - Important tones: 3rd: C, 7th: G

Common chord tones:
- Bm7b5 to E7b9: B, D, F
- E7b9 to Am7: E

Common scale tones:
- B Locrian to E half-whole diminished: B, D, E, F, G
- E half-whole diminished to A Dorian: E, G, B, D

Resolution idea: Use b9 and diminished passing tones as tension, then land on tonic chord tones.

### Tritone substitution option

- **Bm7b5**
  - Function: II in minor
  - Chord tones: B, D, F, A
  - Suggested scale: B Locrian
  - Important tones: 3rd: D, 7th: A
- **Bb7**
  - Function: dominant
  - Chord tones: Bb, D, F, Ab
  - Suggested scale: Bb Lydian dominant
  - Important tones: 3rd: D, 7th: Ab
- **Am7**
  - Function: I in minor
  - Chord tones: A, C, E, G
  - Suggested scale: A Dorian
  - Important tones: 3rd: C, 7th: G

Common chord tones:
- Bm7b5 to Bb7: D, F
- Bb7 to Am7: none

Common scale tones:
- B Locrian to Bb Lydian dominant: C, D, E, F, G
- Bb Lydian dominant to A Dorian: C, D, E, G

Resolution idea: Move the substitute dominant by half step into the tonic root or 5th.
