import os
import re

from instruments import guitar_fretboard, piano_view

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

SCALE_INTERVALS = {
    "Ionian": [0, 2, 4, 5, 7, 9, 11],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Aeolian": [0, 2, 3, 5, 7, 8, 10],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Lydian dominant": [0, 2, 4, 6, 7, 9, 10],
    "half-whole diminished": [0, 1, 3, 4, 6, 7, 9, 10],
    "whole-half diminished": [0, 2, 3, 5, 6, 8, 9, 11],
    "altered": [0, 1, 3, 4, 6, 8, 10],
    "phrygian dominant": [0, 1, 4, 5, 7, 8, 10],
    "Locrian": [0, 1, 3, 5, 6, 8, 10],
    "Locrian natural 2": [0, 2, 3, 5, 6, 8, 10],
    "melodic minor": [0, 2, 3, 5, 7, 9, 11],
}

DOMINANT_QUALITIES = {"7", "9", "13", "7b9", "7#9"}
MAJOR_TONIC_QUALITIES = {"maj7", "6", ""}
MINOR_TONIC_QUALITIES = {"m7", "m9", "m6", "m"}
MINOR_PRE_DOMINANT_QUALITIES = {"m7b5"}
MAJOR_PRE_DOMINANT_QUALITIES = {"m7", "m9"}


def read_grid(filename):
    bars = []

    with open(filename) as grid:
        for line in grid:
            for bar in line.split("|"):
                chords = bar.split()

                if chords:
                    bars.append(chords)

    return bars


def flatten_grid(bars):
    chords = []

    for bar in bars:
        chords.extend(bar)

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


def scale_notes(root, scale):
    root_index = NOTES.index(root)

    return [
        NOTES[(root_index + interval) % 12]
        for interval in SCALE_INTERVALS[scale]
    ]


def suggested_scales(symbol):
    root, quality = parse_chord_symbol(symbol)

    return [
        f"{root} {scale}"
        for scale in SCALE_SUGGESTIONS.get(quality, [])
    ]


def primary_scale(symbol):
    scales = suggested_scales(symbol)

    return scales[0] if scales else None


def common_notes(notes_a, notes_b):
    return [note for note in notes_a if note in notes_b]


def common_tones(chord_a, chord_b):
    tones_a = chord_tones(chord_a)
    tones_b = chord_tones(chord_b)

    return common_notes(tones_a, tones_b)


def transpose_note(note, semitones):
    note_index = NOTES.index(note)

    return NOTES[(note_index + semitones) % 12]


def interval_between(root_a, root_b):
    return (NOTES.index(root_b) - NOTES.index(root_a)) % 12


def chord_quality(symbol):
    return parse_chord_symbol(symbol)[1]


def chord_root(symbol):
    return parse_chord_symbol(symbol)[0]


def is_dominant(symbol):
    return chord_quality(symbol) in DOMINANT_QUALITIES


def is_major_tonic(symbol):
    return chord_quality(symbol) in MAJOR_TONIC_QUALITIES


def is_minor_tonic(symbol):
    return chord_quality(symbol) in MINOR_TONIC_QUALITIES


def chord_function(symbol, key_root=None, key_type="major"):
    root, quality = parse_chord_symbol(symbol)

    if key_root:
        interval = interval_between(key_root, root)

        if (
            key_type == "major"
            and interval == 2
            and quality in MAJOR_PRE_DOMINANT_QUALITIES
        ):
            return "II in major"
        if (
            key_type == "major"
            and interval == 0
            and is_major_tonic(symbol)
        ):
            return "I in major"
        if (
            key_type == "minor"
            and interval == 2
            and quality in MINOR_PRE_DOMINANT_QUALITIES
        ):
            return "II in minor"
        if (
            key_type == "minor"
            and interval == 0
            and is_minor_tonic(symbol)
        ):
            return "I in minor"
        if interval == 7 and is_dominant(symbol):
            return f"V in {key_type}"

    if is_dominant(symbol):
        return "dominant"
    if quality in MAJOR_PRE_DOMINANT_QUALITIES:
        return "minor seventh color"
    if quality in MINOR_PRE_DOMINANT_QUALITIES:
        return "half-diminished pre-dominant"
    if is_major_tonic(symbol):
        return "major tonic color"
    if is_minor_tonic(symbol):
        return "minor tonic color"

    return "chord color"


def important_tones(symbol):
    root, quality = parse_chord_symbol(symbol)
    root_index = NOTES.index(root)
    labels = [
        ("3rd", 3 if quality in {"m7", "m9", "m6", "m", "m7b5", "dim7"} else 4),
        ("7th", 9 if quality == "dim7" else 10),
    ]

    if quality in {"maj7"}:
        labels[1] = ("7th", 11)
    if quality in {"6", "m6", "", "m"}:
        labels = labels[:1]
    if quality in {"9", "m9", "13"}:
        labels.append(("9th", 14))
    if quality == "7b9":
        labels.append(("b9", 13))
    if quality == "7#9":
        labels.append(("#9", 15))
    if quality == "13":
        labels.append(("13th", 21))

    return [
        f"{label}: {NOTES[(root_index + interval) % 12]}"
        for label, interval in labels
    ]


def important_tone_map(symbol):
    root, quality = parse_chord_symbol(symbol)
    root_index = NOTES.index(root)
    intervals = {
        "R": 0,
        "3": 3 if quality in {"m7", "m9", "m6", "m", "m7b5", "dim7"} else 4,
        "5": 6 if quality in {"m7b5", "dim7"} else 7,
    }

    if quality in {"maj7"}:
        intervals["7"] = 11
    elif quality == "dim7":
        intervals["7"] = 9
    elif quality not in {"6", "m6", "", "m"}:
        intervals["7"] = 10

    if quality in {"9", "m9", "13"}:
        intervals["9"] = 14
    if quality == "7b9":
        intervals["b9"] = 13
    if quality == "7#9":
        intervals["#9"] = 15
    if quality == "13":
        intervals["13"] = 21

    return {
        NOTES[(root_index + interval) % 12]: label
        for label, interval in intervals.items()
    }


def scale_tone_map(root, scale):
    root_index = NOTES.index(root)
    intervals = {"R": 0}

    if scale in {"Lydian", "Lydian dominant"}:
        intervals["#11"] = 6
    if scale in {"altered", "half-whole diminished"}:
        intervals["b9"] = 1
        intervals["#9"] = 3
    if scale == "altered":
        intervals["b13"] = 8
    if scale == "phrygian dominant":
        intervals["b9"] = 1

    return {
        NOTES[(root_index + interval) % 12]: label
        for label, interval in intervals.items()
    }


def scale_notes_for_suggestion(suggestion):
    root, scale = suggestion.split(" ", 1)

    return scale_notes(root, scale)


def detect_ii_v_i(chords):
    movements = []

    # These patterns are intentionally small: root motion by fourth/fifth plus broad chord quality.
    for index in range(len(chords) - 2):
        first, second, third = chords[index:index + 3]
        first_root = chord_root(first)
        second_root = chord_root(second)
        third_root = chord_root(third)

        roots_move_by_fourths = (
            interval_between(first_root, second_root) == 5
            and interval_between(second_root, third_root) == 5
        )

        if not roots_move_by_fourths or not is_dominant(second):
            continue

        if (
            chord_quality(first) in MAJOR_PRE_DOMINANT_QUALITIES
            and is_major_tonic(third)
        ):
            movements.append({
                "type": "II-V-I major",
                "chords": [first, second, third],
                "start": index,
                "key": third_root,
            })

        if (
            chord_quality(first) in MINOR_PRE_DOMINANT_QUALITIES
            and is_minor_tonic(third)
        ):
            movements.append({
                "type": "II-V-I minor",
                "chords": [first, second, third],
                "start": index,
                "key": third_root,
            })

    return movements


def detect_secondary_dominants(chords):
    movements = []

    for index, chord in enumerate(chords[:-1]):
        next_chord = chords[index + 1]

        if not is_dominant(chord):
            continue

        if interval_between(chord_root(chord), chord_root(next_chord)) == 5:
            movements.append({
                "type": "secondary dominant",
                "chords": [chord, next_chord],
                "start": index,
                "target": next_chord,
            })

    return movements


def detect_tritone_substitutions(chords):
    movements = []

    for index, chord in enumerate(chords):
        if is_dominant(chord):
            substitute = f"{transpose_note(chord_root(chord), 6)}7"
            movements.append({
                "type": "tritone substitution candidate",
                "chords": [chord],
                "start": index,
                "substitute": substitute,
            })

    return movements


def detect_harmonic_movements(chords):
    return (
        detect_ii_v_i(chords)
        + detect_secondary_dominants(chords)
        + detect_tritone_substitutions(chords)
    )


def ii_v_i_options(movement):
    first, second, third = movement["chords"]
    dominant_root = chord_root(second)
    tritone_sub = f"{transpose_note(dominant_root, 6)}7"
    key_type = "minor" if movement["type"] == "II-V-I minor" else "major"
    inside_dominant_scale = (
        f"{dominant_root} phrygian dominant"
        if key_type == "minor"
        else f"{dominant_root} Mixolydian"
    )

    return [
        {
            "name": "Inside / diatonic option",
            "chords": [first, second, third],
            "scales": {
                first: primary_scale(first),
                second: inside_dominant_scale,
                third: primary_scale(third),
            },
            "resolution": "Keep guide tones clear: the dominant 7th resolves down, and the dominant 3rd resolves toward the tonic.",
        },
        {
            "name": "Altered dominant option",
            "chords": [first, f"{dominant_root}7#9", third],
            "scales": {
                first: primary_scale(first),
                f"{dominant_root}7#9": f"{dominant_root} altered",
                third: primary_scale(third),
            },
            "resolution": "Resolve #9/b9 colors by half step into stable chord tones on the tonic.",
        },
        {
            "name": "Half-whole diminished dominant option",
            "chords": [first, f"{dominant_root}7b9", third],
            "scales": {
                first: primary_scale(first),
                f"{dominant_root}7b9": f"{dominant_root} half-whole diminished",
                third: primary_scale(third),
            },
            "resolution": "Use b9 and diminished passing tones as tension, then land on tonic chord tones.",
        },
        {
            "name": "Tritone substitution option",
            "chords": [first, tritone_sub, third],
            "scales": {
                first: primary_scale(first),
                tritone_sub: f"{chord_root(tritone_sub)} Lydian dominant",
                third: primary_scale(third),
            },
            "resolution": "Move the substitute dominant by half step into the tonic root or 5th.",
        },
    ]


def format_notes(notes):
    return ", ".join(notes) if notes else "none"


def format_grid(bars):
    return "\n".join(f"| {' '.join(bar)} |" for bar in bars)


def markdown_chord_summary(chord):
    scales = suggested_scales(chord)

    return [
        f"- **{chord}**",
        f"  - Function: {chord_function(chord)}",
        f"  - Chord tones: {format_notes(chord_tones(chord))}",
        f"  - Suggested scales: {', '.join(scales) if scales else 'none'}",
        f"  - Important tones: {format_notes(important_tones(chord))}",
    ]


def markdown_option(option, key_root, key_type):
    lines = [f"### {option['name']}", ""]
    chords = option["chords"]

    for chord in chords:
        scale = option["scales"].get(chord)
        scale_text = scale if scale else "none"
        lines.extend([
            f"- **{chord}**",
            f"  - Function: {chord_function(chord, key_root, key_type)}",
            f"  - Chord tones: {format_notes(chord_tones(chord))}",
            f"  - Suggested scale: {scale_text}",
            f"  - Important tones: {format_notes(important_tones(chord))}",
        ])

    lines.append("")
    lines.append("Common chord tones:")

    for first, second in zip(chords, chords[1:]):
        lines.append(
            f"- {first} to {second}: {format_notes(common_tones(first, second))}"
        )

    lines.append("")
    lines.append("Common scale tones:")

    for first, second in zip(chords, chords[1:]):
        first_scale = option["scales"].get(first)
        second_scale = option["scales"].get(second)

        if first_scale and second_scale:
            common = common_notes(
                scale_notes_for_suggestion(first_scale),
                scale_notes_for_suggestion(second_scale),
            )
        else:
            common = []

        lines.append(f"- {first_scale} to {second_scale}: {format_notes(common)}")

    lines.extend([
        "",
        f"Resolution idea: {option['resolution']}",
        "",
    ])

    return lines


def generate_markdown_report(bars, original_grid=None):
    chords = flatten_grid(bars)
    movements = detect_harmonic_movements(chords)
    ii_v_i_movements = [
        movement for movement in movements
        if movement["type"] in {"II-V-I major", "II-V-I minor"}
    ]
    lines = [
        "# Jazz Harmony Analysis",
        "",
        "## 1. Original grid",
        "",
        "```text",
        original_grid.strip() if original_grid else format_grid(bars),
        "```",
        "",
        "## 2. Parsed chords by bar",
        "",
    ]

    for index, bar in enumerate(bars, start=1):
        lines.append(f"- Bar {index}: {', '.join(bar)}")

    lines.extend([
        "",
        "## 3. Chord tones for each chord",
        "",
    ])

    for chord in chords:
        lines.extend(markdown_chord_summary(chord))

    lines.extend([
        "",
        "## 4. Detected harmonic movements",
        "",
    ])

    if movements:
        for movement in movements:
            chord_text = " -> ".join(movement["chords"])
            details = ""

            if "key" in movement:
                details = f" in {movement['key']}"
            if "target" in movement:
                details = f" resolving to {movement['target']}"
            if "substitute" in movement:
                details = f": try {movement['substitute']}"

            lines.append(f"- {movement['type']}: {chord_text}{details}")
    else:
        lines.append("- No common movements detected yet.")

    lines.extend([
        "",
        "## 5. Harmonic options for detected II-V-I movements",
        "",
    ])

    if ii_v_i_movements:
        for movement in ii_v_i_movements:
            lines.extend([
                f"### {movement['type']} in {movement['key']}: {' -> '.join(movement['chords'])}",
                "",
            ])

            key_type = "minor" if movement["type"] == "II-V-I minor" else "major"

            for option in ii_v_i_options(movement):
                lines.extend(markdown_option(option, movement["key"], key_type))
    else:
        lines.append("No II-V-I movements detected, so no reharmonization options were generated.")

    return "\n".join(lines).rstrip() + "\n"


def write_markdown_report(bars, filename, original_grid=None):
    with open(filename, "w") as report:
        report.write(generate_markdown_report(bars, original_grid))


def parse_scale_suggestion(suggestion):
    root, scale = suggestion.split(" ", 1)

    return root, scale


def scale_filename(suggestion):
    root, scale = parse_scale_suggestion(suggestion)
    clean_scale = scale.lower().replace("-", "_").replace(" ", "_")

    return f"{root}_{clean_scale}.md"


def resolution_idea_for_scale(suggestion, chord):
    _, scale = parse_scale_suggestion(suggestion)

    if scale == "altered":
        return "Aim altered color tones by half step into stable tones on the next chord."
    if scale == "half-whole diminished":
        return "Use diminished color tones as passing tension, then resolve to chord tones."
    if scale == "Lydian dominant":
        return "Lean on #11 color, then resolve the dominant guide tones smoothly."
    if scale == "phrygian dominant":
        return "Treat b9 as a strong pull into the minor tonic sound."
    if is_dominant(chord):
        return "Resolve the 7th down and the 3rd toward the next chord."

    return "Use 3rds and 7ths as landing tones, then connect neighboring scale notes melodically."


def collect_practice_contexts(bars):
    chords = flatten_grid(bars)
    contexts = {}
    chord_scales = [
        {
            "chord": chord,
            "scales": suggested_scales(chord),
        }
        for chord in chords
    ]

    for index, item in enumerate(chord_scales):
        chord = item["chord"]

        for suggestion in item["scales"]:
            context = contexts.setdefault(suggestion, {
                "suggestion": suggestion,
                "chords": [],
                "previous_scales": set(),
                "next_scales": set(),
                "roles": {},
                "resolution_ideas": set(),
            })
            context["chords"].append(chord)
            context["roles"].update(important_tone_map(chord))
            context["resolution_ideas"].add(
                resolution_idea_for_scale(suggestion, chord)
            )

            if index > 0:
                context["previous_scales"].update(chord_scales[index - 1]["scales"])
            if index < len(chord_scales) - 1:
                context["next_scales"].update(chord_scales[index + 1]["scales"])

    for movement in detect_ii_v_i(chords):
        for option in ii_v_i_options(movement):
            option_scales = [
                option["scales"].get(chord)
                for chord in option["chords"]
            ]

            for index, chord in enumerate(option["chords"]):
                suggestion = option_scales[index]

                if not suggestion:
                    continue

                context = contexts.setdefault(suggestion, {
                    "suggestion": suggestion,
                    "chords": [],
                    "previous_scales": set(),
                    "next_scales": set(),
                    "roles": {},
                    "resolution_ideas": set(),
                })

                if chord not in context["chords"]:
                    context["chords"].append(chord)

                context["roles"].update(important_tone_map(chord))

                if index > 0 and option_scales[index - 1]:
                    context["previous_scales"].add(option_scales[index - 1])
                if index < len(option_scales) - 1 and option_scales[index + 1]:
                    context["next_scales"].add(option_scales[index + 1])

                if chord == option["chords"][1]:
                    context["resolution_ideas"].add(option["resolution"])

    return contexts


def common_scale_lines(label, suggestion, related_scales):
    lines = [f"### Common tones with {label} scales", ""]

    if not related_scales:
        lines.extend(["No neighboring scale context found.", ""])
        return lines

    notes = scale_notes_for_suggestion(suggestion)

    for related in sorted(related_scales):
        common = common_notes(notes, scale_notes_for_suggestion(related))
        lines.append(f"- {related}: {format_notes(common)}")

    lines.append("")
    return lines


def markdown_practice_sheet(context):
    suggestion = context["suggestion"]
    root, scale = parse_scale_suggestion(suggestion)
    notes = scale_notes(root, scale)
    notes_with_octave = notes + [root]
    note_roles = dict(context["roles"])
    note_roles.update(scale_tone_map(root, scale))
    target_tones = [
        f"{role}: {note}"
        for note, role in sorted(note_roles.items())
        if note in notes
    ]
    lines = [
        f"# {suggestion} Practice Sheet",
        "",
        "## Scale",
        "",
        f"- Notes: {format_notes(notes_with_octave)}",
        f"- Chord context: {', '.join(context['chords'])}",
        f"- Important tones: {format_notes(target_tones)}",
        "",
    ]

    lines.extend(common_scale_lines(
        "previous",
        suggestion,
        context["previous_scales"],
    ))
    lines.extend(common_scale_lines(
        "next",
        suggestion,
        context["next_scales"],
    ))

    lines.extend([
        "## Resolution ideas",
        "",
    ])

    for idea in sorted(context["resolution_ideas"]):
        lines.append(f"- {idea}")

    lines.append("")
    lines.extend(guitar_fretboard(root, notes, note_roles, transpose_note))
    lines.extend(piano_view(notes_with_octave, target_tones))

    return "\n".join(lines).rstrip() + "\n"


def write_practice_sheets(bars, folder):
    os.makedirs(folder, exist_ok=True)
    contexts = collect_practice_contexts(bars)

    for suggestion, context in contexts.items():
        filename = os.path.join(folder, scale_filename(suggestion))

        with open(filename, "w") as sheet:
            sheet.write(markdown_practice_sheet(context))

    return sorted(scale_filename(suggestion) for suggestion in contexts)


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
