import re

NOTES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

ENHARMONIC = {
    "C#": "Db",
    "D#": "Eb",
    "F#": "Gb",
    "G#": "Ab",
    "A#": "Bb",
}

CHORD_INTERVALS = {
    "maj7": [0, 4, 7, 11],
    "m7b5": [0, 3, 6, 10],
    "dim7": [0, 3, 6, 9],
    "m7": [0, 3, 7, 10],
    "7": [0, 4, 7, 10],
    "m": [0, 3, 7],
    "": [0, 4, 7],
}


def normalize_note(note):
    return ENHARMONIC.get(note, note)


def parse_chord_symbol(symbol):
    match = re.match(r"^([A-G](?:b|#)?)(.*)$", symbol)
    if not match:
        raise ValueError(f"Invalid chord symbol: {symbol}")

    root = normalize_note(match.group(1))
    quality = match.group(2)

    if quality not in CHORD_INTERVALS:
        raise ValueError(f"Unsupported chord quality: {quality}")

    return root, quality


def chord_tones(symbol):
    root, quality = parse_chord_symbol(symbol)
    root_index = NOTES.index(root)

    return [
        NOTES[(root_index + interval) % 12]
        for interval in CHORD_INTERVALS[quality]
    ]


def common_tones(chord_a, chord_b):
    tones_a = chord_tones(chord_a)
    tones_b = chord_tones(chord_b)

    return [note for note in tones_a if note in tones_b]


def analyse_progression(chords):
    print("Chord tones:")
    print()

    for chord in chords:
        print(f"{chord:8} -> {' '.join(chord_tones(chord))}")

    print()
    print("Common tones:")
    print()

    for first, second in zip(chords, chords[1:]):
        common = common_tones(first, second)
        common_text = ", ".join(common) if common else "none"
        print(f"{first:8} -> {second:8}: {common_text}")