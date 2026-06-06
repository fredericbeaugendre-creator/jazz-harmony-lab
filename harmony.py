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
    "m7": [0, 3, 7, 10],
    "7": [0, 4, 7, 10],
    "m7b5": [0, 3, 6, 10],
    "dim7": [0, 3, 6, 9],
    "6": [0, 4, 7, 9],
    "m6": [0, 3, 7, 9],
    "9": [0, 4, 7, 10, 14],
    "m9": [0, 3, 7, 10, 14],
    "13": [0, 4, 7, 10, 14, 21],
    "7b9": [0, 4, 7, 10, 13],
    "7#9": [0, 4, 7, 10, 15],
    "m": [0, 3, 7],
    "": [0, 4, 7],
}

SCALE_SUGGESTIONS = {
    "maj7": ["Ionian", "Lydian"],
    "m7": ["Dorian", "Aeolian"],
    "7": ["Mixolydian", "Lydian dominant"],
    "m7b5": ["Locrian", "Locrian natural 2"],
    "dim7": ["whole-half diminished"],
    "6": ["Ionian", "Lydian"],
    "m6": ["melodic minor", "Dorian"],
    "9": ["Mixolydian", "Lydian dominant"],
    "m9": ["Dorian", "Aeolian"],
    "13": ["Mixolydian", "Lydian dominant"],
    "7b9": ["half-whole diminished", "altered", "phrygian dominant"],
    "7#9": ["altered", "half-whole diminished"],
    "m": ["Dorian", "Aeolian"],
    "": ["Ionian"],
}


def read_grid(filename):
    chords = []

    with open(filename) as grid:
        for line in grid:
            bars = line.split("|")

            for bar in bars:
                chords.extend(bar.split())

    return chords


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


def suggested_scales(symbol):
    root, quality = parse_chord_symbol(symbol)

    return [
        f"{root} {scale}"
        for scale in SCALE_SUGGESTIONS.get(quality, [])
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
    print("Suggested scales:")
    print()

    for chord in chords:
        scales = suggested_scales(chord)
        scales_text = ", ".join(scales) if scales else "none"
        print(f"{chord:8} -> {scales_text}")

    print()
    print("Common tones:")
    print()

    for first, second in zip(chords, chords[1:]):
        common = common_tones(first, second)
        common_text = ", ".join(common) if common else "none"
        print(f"{first:8} -> {second:8}: {common_text}")
