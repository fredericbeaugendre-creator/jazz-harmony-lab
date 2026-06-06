GUITAR_STRINGS = ["E", "B", "G", "D", "A", "E"]


def guitar_fretboard(root, scale_notes, note_roles, transpose_note):
    lines = [
        "### Guitar fretboard",
        "",
        "Frets 0-12. `R`, `3`, `5`, `7`, `9`, `b9`, `#9`, `#11`, and `b13` mark target tones when available; `o` marks another scale tone.",
        "",
        "```text",
        "       " + " ".join(f"{fret:>3}" for fret in range(13)),
    ]

    for string in GUITAR_STRINGS:
        cells = []

        for fret in range(13):
            note = transpose_note(string, fret)

            if note in scale_notes:
                cells.append(f"{note_roles.get(note, 'o'):>3}")
            else:
                cells.append("  .")

        lines.append(f"{string:>2} | " + " ".join(cells))

    lines.extend(["```", ""])

    return lines


def piano_fingering(scale_notes):
    if len(scale_notes) == 9:
        return ["1", "2", "3", "1", "2", "3", "4", "1", "5"]

    if len(scale_notes) == 8:
        return ["1", "2", "3", "1", "2", "3", "4", "5"]

    pattern = ["1", "2", "3", "1", "2", "3", "4"]
    return pattern[:len(scale_notes)]


def piano_view(scale_notes, target_tones):
    fingering = piano_fingering(scale_notes)
    lines = [
        "### Piano view",
        "",
        f"- Scale notes: {', '.join(scale_notes)}",
        f"- Suggested RH fingering: {'-'.join(fingering)}",
        "- Fingering is a starting point, not a rule. Adjust it for tempo, line direction, and hand shape.",
        f"- Target tones: {', '.join(target_tones) if target_tones else 'none'}",
        "",
    ]

    return lines
