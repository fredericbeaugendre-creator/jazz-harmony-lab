import os

GUITAR_STRINGS = ["E", "B", "G", "D", "A", "E"]
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


def svg_escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def role_color(role):
    return ROLE_COLORS.get(role, ROLE_COLORS["o"])


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as svg:
        svg.write(content)


def guitar_svg(root, scale_name, scale_notes, note_roles, transpose_note):
    width = 980
    height = 360
    left = 76
    right = 36
    top = 76
    string_gap = 34
    fret_gap = (width - left - right) / 12
    board_height = string_gap * 5
    title = f"{root} {scale_name} - Guitar"
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="{left}" y="34" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#0f172a">{svg_escape(title)}</text>',
        f'<text x="{left}" y="56" font-family="Arial, sans-serif" font-size="13" fill="#475569">Frets 0-12. Important tones use labels; other scale tones are small note names.</text>',
        f'<rect x="{left}" y="{top - 14}" width="{width - left - right}" height="{board_height + 28}" rx="10" fill="#fff7ed" stroke="#c2410c" stroke-width="1.2"/>',
    ]

    for fret in range(13):
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

    for index, string in enumerate(GUITAR_STRINGS):
        y = top + index * string_gap
        stroke_width = 1.2 + index * 0.25
        elements.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" stroke="#334155" stroke-width="{stroke_width:.1f}"/>'
        )
        elements.append(
            f'<text x="{left - 24}" y="{y + 4:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#334155">{string}</text>'
        )

        for fret in range(13):
            note = transpose_note(string, fret)

            if note not in scale_notes:
                continue

            cx = left + fret * fret_gap if fret == 0 else left + (fret - 0.5) * fret_gap
            role = note_roles.get(note, "o")
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


def write_guitar_svg(path, root, scale_name, scale_notes, note_roles, transpose_note):
    write_file(path, guitar_svg(root, scale_name, scale_notes, note_roles, transpose_note))


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
        active = note in scale_notes
        role = note_roles.get(note, "o")
        fill = "#dbeafe" if active else "#ffffff"
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
            active = note in scale_notes
            role = note_roles.get(note, "o")
            fill = "#475569" if active and role == "o" else role_color(role)

            if not active:
                fill = "#111827"

            stroke = "#0f172a"

            elements.append(
                f'<rect x="{x}" y="{top}" width="{black_width}" height="{black_height}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            )

            if active:
                label = note if role == "o" else role
                elements.append(
                    f'<text x="{x + black_width / 2}" y="{top + black_height - 16}" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#ffffff">{svg_escape(label)}</text>'
                )

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


def diagram_markdown(guitar_path, piano_path):
    return [
        "## Diagrams",
        "",
        "### Guitar fretboard",
        "",
        f"![Guitar fretboard]({guitar_path})",
        "",
        "### Piano keyboard",
        "",
        f"![Piano keyboard]({piano_path})",
        "",
    ]


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
