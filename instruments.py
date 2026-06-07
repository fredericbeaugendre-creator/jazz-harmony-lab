import os
import re

GUITAR_STRINGS = ["E", "B", "G", "D", "A", "E"]
BASS_4_STRINGS = ["G", "D", "A", "E"]
BASS_5_STRINGS = ["G", "D", "A", "E", "B"]
WHITE_KEYS = ["C", "D", "E", "F", "G", "A", "B"]
BLACK_KEYS = {
    "Db": 0,
    "Eb": 1,
    "Gb": 3,
    "Ab": 4,
    "Bb": 5,
}

ROLE_COLORS = {
    "R": "#2563eb",
    "3": "#16a34a",
    "5": "#64748b",
    "7": "#9333ea",
    "9": "#0891b2",
    "b9": "#dc2626",
    "#9": "#ea580c",
    "#11": "#ca8a04",
    "b13": "#be123c",
    "13": "#0f766e",
    "o": "#f8fafc",
}

ORDINARY_SCALE_FILL = "#e0f2fe"
ORDINARY_SCALE_STROKE = "#0284c7"
INACTIVE_WHITE_KEY_FILL = "#dbeafe"
ACTIVE_BLACK_KEY_FILL = "#1e3a5f"
INACTIVE_BLACK_KEY_FILL = "#111827"

NOTE_PITCH_CLASSES = {
    "C": 0,
    "B#": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "Fb": 4,
    "E#": 5,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
    "Cb": 11,
}
NATURAL_NOTE_PITCH_CLASSES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
ACCIDENTAL_OFFSETS = {
    "bb": -2,
    "b": -1,
    "": 0,
    "#": 1,
    "##": 2,
}


def svg_escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def role_color(role):
    return ROLE_COLORS.get(role, ROLE_COLORS["o"])


def note_pitch_class(note):
    if note in NOTE_PITCH_CLASSES:
        return NOTE_PITCH_CLASSES[note]

    match = re.match(r"^([A-G])([b#]{0,2})$", note)

    if not match or match.group(2) not in ACCIDENTAL_OFFSETS:
        raise ValueError(f"Invalid note name: {note}")

    letter, accidental = match.groups()

    return (NATURAL_NOTE_PITCH_CLASSES[letter] + ACCIDENTAL_OFFSETS[accidental]) % 12


def contains_pitch(notes, note):
    pitch_class = note_pitch_class(note)

    return any(note_pitch_class(item) == pitch_class for item in notes)


def pitch_role(note, note_roles):
    pitch_class = note_pitch_class(note)

    for role_note, role in note_roles.items():
        if note_pitch_class(role_note) == pitch_class:
            return role

    return "o"


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as svg:
        svg.write(content)


def fretted_instrument_svg(
    instrument_name,
    tuning,
    root,
    scale_name,
    scale_notes,
    note_roles,
    transpose_note,
    fret_count=12,
):
    width = 980
    height = 260 + 34 * len(tuning)
    left = 76
    right = 36
    top = 76
    string_gap = 34
    fret_gap = (width - left - right) / fret_count
    board_height = string_gap * (len(tuning) - 1)
    title = f"{root} {scale_name} - {instrument_name}"
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="{left}" y="34" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#0f172a">{svg_escape(title)}</text>',
        f'<text x="{left}" y="56" font-family="Arial, sans-serif" font-size="13" fill="#475569">Frets 0-12. Important tones use labels; other scale tones are small note names.</text>',
        f'<rect x="{left}" y="{top - 14}" width="{width - left - right}" height="{board_height + 28}" rx="10" fill="#fff7ed" stroke="#c2410c" stroke-width="1.2"/>',
    ]

    for fret in range(fret_count + 1):
        x = left + fret * fret_gap
        stroke_width = 5 if fret == 0 else 1.4
        color = "#7c2d12" if fret == 0 else "#9a3412"
        elements.append(
            f'<line x1="{x:.1f}" y1="{top - 14}" x2="{x:.1f}" y2="{top + board_height + 14}" stroke="{color}" stroke-width="{stroke_width}"/>'
        )

        if fret > 0:
            label_x = left + (fret - 0.5) * fret_gap
            elements.append(
                f'<text x="{label_x:.1f}" y="{top + board_height + 42}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#64748b">{fret}</text>'
            )

    for index, string in enumerate(tuning):
        y = top + index * string_gap
        stroke_width = 1.2 + index * 0.25
        elements.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" stroke="#334155" stroke-width="{stroke_width:.1f}"/>'
        )
        elements.append(
            f'<text x="{left - 24}" y="{y + 4:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#334155">{string}</text>'
        )

        for fret in range(fret_count + 1):
            note = transpose_note(string, fret)

            if not contains_pitch(scale_notes, note):
                continue

            cx = left + fret * fret_gap if fret == 0 else left + (fret - 0.5) * fret_gap
            role = pitch_role(note, note_roles)
            fill = role_color(role)
            stroke = "#334155" if role == "o" else "#0f172a"
            text = note if role == "o" else role
            text_color = "#0f172a" if role == "o" else "#ffffff"
            radius = 11 if role == "o" else 15

            elements.extend([
                f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>',
                f'<text x="{cx:.1f}" y="{y + 4:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{text_color}">{svg_escape(text)}</text>',
            ])

    legend_items = [
        ("R", "root"),
        ("3", "third"),
        ("5", "fifth"),
        ("7", "seventh"),
        ("b9", "flat nine"),
        ("#9", "sharp nine"),
        ("#11", "sharp eleven"),
        ("b13", "flat thirteen"),
    ]
    x = left
    y = height - 32

    for role, label in legend_items:
        elements.extend([
            f'<circle cx="{x}" cy="{y}" r="9" fill="{role_color(role)}"/>',
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" font-weight="700" fill="#ffffff">{role}</text>',
            f'<text x="{x + 14}" y="{y + 4}" font-family="Arial, sans-serif" font-size="11" fill="#475569">{label}</text>',
        ])
        x += 92

    elements.append("</svg>")
    return "\n".join(elements) + "\n"


def guitar_svg(root, scale_name, scale_notes, note_roles, transpose_note):
    return fretted_instrument_svg(
        "Guitar",
        GUITAR_STRINGS,
        root,
        scale_name,
        scale_notes,
        note_roles,
        transpose_note,
    )


def write_guitar_svg(path, root, scale_name, scale_notes, note_roles, transpose_note):
    write_file(path, guitar_svg(root, scale_name, scale_notes, note_roles, transpose_note))


def write_bass_4_svg(path, root, scale_name, scale_notes, note_roles, transpose_note):
    write_file(path, fretted_instrument_svg(
        "4-string Bass",
        BASS_4_STRINGS,
        root,
        scale_name,
        scale_notes,
        note_roles,
        transpose_note,
    ))


def write_bass_5_svg(path, root, scale_name, scale_notes, note_roles, transpose_note):
    write_file(path, fretted_instrument_svg(
        "5-string Bass",
        BASS_5_STRINGS,
        root,
        scale_name,
        scale_notes,
        note_roles,
        transpose_note,
    ))


def piano_fingering(scale_notes):
    if len(scale_notes) == 9:
        return ["1", "2", "3", "1", "2", "3", "4", "1", "5"]

    if len(scale_notes) == 8:
        return ["1", "2", "3", "1", "2", "3", "4", "5"]

    pattern = ["1", "2", "3", "1", "2", "3", "4"]
    return pattern[:len(scale_notes)]


def piano_svg(root, scale_name, scale_notes, note_roles):
    white_width = 52
    white_height = 190
    black_width = 34
    black_height = 116
    left = 42
    top = 84
    width = left * 2 + white_width * 14
    height = 340
    title = f"{root} {scale_name} - Piano"
    white_notes = WHITE_KEYS * 2
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="{left}" y="34" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#0f172a">{svg_escape(title)}</text>',
        f'<text x="{left}" y="56" font-family="Arial, sans-serif" font-size="13" fill="#475569">Only scale tones are marked. Large circles are target tones; small diamonds are other scale tones.</text>',
    ]

    for index, note in enumerate(white_notes):
        x = left + index * white_width
        active = contains_pitch(scale_notes, note)
        role = pitch_role(note, note_roles)
        fill = "#ffffff" if active else INACTIVE_WHITE_KEY_FILL
        stroke = "#2563eb" if active else "#94a3b8"

        elements.append(
            f'<rect x="{x}" y="{top}" width="{white_width}" height="{white_height}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
        )
        elements.append(
            f'<text x="{x + white_width / 2}" y="{top + white_height - 16}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#334155">{note}</text>'
        )

        if active:
            cx = x + white_width / 2

            if role == "o":
                diamond_points = [
                    (cx, top + white_height - 64),
                    (cx + 8, top + white_height - 54),
                    (cx, top + white_height - 44),
                    (cx - 8, top + white_height - 54),
                ]
                points = " ".join(f"{x},{y}" for x, y in diamond_points)
                elements.extend([
                    f'<polygon points="{points}" fill="{ORDINARY_SCALE_FILL}" stroke="{ORDINARY_SCALE_STROKE}" stroke-width="1.2"/>',
                    f'<text x="{cx}" y="{top + white_height - 34}" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#0369a1">{note}</text>',
                ])
            else:
                elements.extend([
                    f'<circle cx="{cx}" cy="{top + white_height - 54}" r="15" fill="{role_color(role)}" stroke="#0f172a" stroke-width="1"/>',
                    f'<text x="{cx}" y="{top + white_height - 50}" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#ffffff">{svg_escape(role)}</text>',
                ])

    for octave in range(2):
        offset = left + octave * white_width * 7

        for note, white_index in BLACK_KEYS.items():
            x = offset + (white_index + 1) * white_width - black_width / 2
            active = contains_pitch(scale_notes, note)
            role = pitch_role(note, note_roles)

            fill = ACTIVE_BLACK_KEY_FILL if active else INACTIVE_BLACK_KEY_FILL
            elements.append(
                f'<rect x="{x}" y="{top}" width="{black_width}" height="{black_height}" rx="4" fill="{fill}" stroke="#0f172a" stroke-width="1"/>'
            )

            if active:
                cx = x + black_width / 2

                if role == "o":
                    diamond_points = [
                        (cx, top + black_height - 54),
                        (cx + 8, top + black_height - 44),
                        (cx, top + black_height - 34),
                        (cx - 8, top + black_height - 44),
                    ]
                    points = " ".join(f"{x},{y}" for x, y in diamond_points)
                    elements.extend([
                        f'<polygon points="{points}" fill="{ORDINARY_SCALE_FILL}" stroke="{ORDINARY_SCALE_STROKE}" stroke-width="1.2"/>',
                        f'<text x="{cx}" y="{top + black_height - 14}" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#bae6fd">{svg_escape(note)}</text>',
                    ])
                else:
                    elements.extend([
                        f'<circle cx="{cx}" cy="{top + black_height - 44}" r="14" fill="{role_color(role)}" stroke="#f8fafc" stroke-width="1.2"/>',
                        f'<text x="{cx}" y="{top + black_height - 40}" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#ffffff">{svg_escape(role)}</text>',
                    ])

    fingering = "-".join(piano_fingering(scale_notes + [root]))
    elements.extend([
        f'<circle cx="{left + 10}" cy="{height - 58}" r="10" fill="{role_color("R")}" stroke="#0f172a" stroke-width="1"/>',
        f'<text x="{left + 10}" y="{height - 54}" text-anchor="middle" font-family="Arial, sans-serif" font-size="8" font-weight="700" fill="#ffffff">R</text>',
        f'<text x="{left + 26}" y="{height - 54}" font-family="Arial, sans-serif" font-size="11" fill="#475569">important tone</text>',
        f'<polygon points="{left + 156},{height - 68} {left + 164},{height - 58} {left + 156},{height - 48} {left + 148},{height - 58}" fill="{ORDINARY_SCALE_FILL}" stroke="{ORDINARY_SCALE_STROKE}" stroke-width="1.2"/>',
        f'<text x="{left + 176}" y="{height - 54}" font-family="Arial, sans-serif" font-size="11" fill="#475569">other scale tone</text>',
        f'<text x="{left}" y="{height - 22}" font-family="Arial, sans-serif" font-size="13" fill="#334155">Suggested RH fingering: {svg_escape(fingering)}. Treat this as a starting point.</text>',
        "</svg>",
    ])
    return "\n".join(elements) + "\n"


def write_piano_svg(path, root, scale_name, scale_notes, note_roles):
    write_file(path, piano_svg(root, scale_name, scale_notes, note_roles))


def diagram_markdown(guitar_path, piano_path, bass_4_path=None, bass_5_path=None):
    lines = [
        "## Diagrams",
        "",
        "### Guitar fretboard",
        "",
        f"![Guitar fretboard]({guitar_path})",
        "",
    ]

    if bass_4_path and bass_5_path:
        lines.extend([
            "## Electric Bass",
            "",
            "### 4-string bass",
            "",
            f"![4-string bass fretboard]({bass_4_path})",
            "",
            "### 5-string bass",
            "",
            f"![5-string bass fretboard]({bass_5_path})",
            "",
        ])

    lines.extend([
        "### Piano keyboard",
        "",
        f"![Piano keyboard]({piano_path})",
        "",
    ])

    return lines


def piano_view(scale_notes, target_tones):
    fingering = piano_fingering(scale_notes)
    return [
        "## Piano notes",
        "",
        f"- Scale notes: {', '.join(scale_notes)}",
        f"- Suggested RH fingering: {'-'.join(fingering)}",
        "- Fingering is a starting point, not a rule. Adjust it for tempo, line direction, and hand shape.",
        f"- Target tones: {', '.join(target_tones) if target_tones else 'none'}",
        "",
    ]
