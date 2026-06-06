# Jazz Harmony Lab

A small Python tool to analyse jazz chord progressions.

## First goals

- Parse chord symbols such as Fmaj7, Gm7, C7, Dm7b5
- Display chord tones
- Find common tones between consecutive chords
- Detect simple jazz progressions such as II-V-I
- Help with composition and improvisation

## Example

Input:

| Fmaj7 | Gm7 C7 | Fmaj7 |

Output:

Fmaj7 -> F A C E  
Gm7 -> G Bb D F  
C7 -> C E G Bb  

Common tones:

Fmaj7 to Gm7: F  
Gm7 to C7: G, Bb  
C7 to Fmaj7: C, E