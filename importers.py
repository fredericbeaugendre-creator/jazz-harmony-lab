import xml.etree.ElementTree as ET

MUSICXML_KIND_MAP = {
    "major": "",
    "minor": "m",
    "major-seventh": "maj7",
    "minor-seventh": "m7",
    "dominant": "7",
    "dominant-seventh": "7",
    "minor-major-seventh": "mMaj7",
    "half-diminished": "m7b5",
    "diminished-seventh": "dim7",
    "major-sixth": "6",
    "minor-sixth": "m6",
    "dominant-ninth": "9",
    "minor-ninth": "m9",
    "dominant-13th": "13",
}

ALTER_TO_ACCIDENTAL = {
    -2: "bb",
    -1: "b",
    0: "",
    1: "#",
    2: "##",
}


def read_grid_file(filename):
    bars = []

    with open(filename) as grid:
        for line in grid:
            for bar in line.split("|"):
                chords = bar.split()

                if chords:
                    bars.append(chords)

    return bars


def xml_text(element, path):
    found = element.find(path)

    if found is None or found.text is None:
        return ""

    return found.text.strip()


def parse_alter(value):
    if not value:
        return 0

    return int(float(value))


def accidental_from_alter(alter):
    return ALTER_TO_ACCIDENTAL.get(alter, "")


def musicxml_root(harmony):
    step = xml_text(harmony, "root/root-step")
    alter = parse_alter(xml_text(harmony, "root/root-alter"))

    return f"{step}{accidental_from_alter(alter)}"


def musicxml_bass(harmony):
    step = xml_text(harmony, "bass/bass-step")

    if not step:
        return ""

    alter = parse_alter(xml_text(harmony, "bass/bass-alter"))
    return f"/{step}{accidental_from_alter(alter)}"


def musicxml_kind(harmony):
    kind = harmony.find("kind")

    if kind is None:
        return ""

    value = kind.attrib.get("text") or kind.text or ""
    value = value.strip()

    if value in {"", "major"}:
        return ""

    if value in MUSICXML_KIND_MAP:
        return MUSICXML_KIND_MAP[value]

    compact = value.replace(" ", "").replace("-", "")

    if compact in {"maj7", "m7", "m7b5", "dim7", "m6", "m9", "13", "9", "7"}:
        return compact

    return value


def musicxml_degrees(harmony):
    suffix = ""

    for degree in harmony.findall("degree"):
        value = xml_text(degree, "degree-value")
        alter = parse_alter(xml_text(degree, "degree-alter"))
        degree_type = xml_text(degree, "degree-type")

        if degree_type not in {"add", "alter"}:
            continue

        suffix += f"{accidental_from_alter(alter)}{value}"

    return suffix


def musicxml_chord_symbol(harmony):
    root = musicxml_root(harmony)

    if not root:
        return ""

    return root + musicxml_kind(harmony) + musicxml_degrees(harmony) + musicxml_bass(harmony)


def strip_namespace(tree):
    for element in tree.iter():
        if "}" in element.tag:
            element.tag = element.tag.split("}", 1)[1]


def read_musicxml_file(filename):
    tree = ET.parse(filename)
    strip_namespace(tree)
    bars = []

    for measure in tree.findall(".//measure"):
        chords = []

        for harmony in measure.findall("harmony"):
            symbol = musicxml_chord_symbol(harmony)

            if symbol:
                chords.append(symbol)

        if chords:
            bars.append(chords)

    return bars


def read_irealb_url(_url):
    raise NotImplementedError("irealb:// import is planned but not implemented yet.")
