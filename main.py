import argparse

from harmony import format_grid, write_markdown_report, write_practice_sheets
from importers import read_grid_file, read_musicxml_file


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate jazz harmony analysis and practice sheets."
    )
    parser.add_argument(
        "--grid",
        default="grid.txt",
        help="Read a simple bar-separated chord grid. Defaults to grid.txt.",
    )
    parser.add_argument(
        "--musicxml",
        help="Read chord symbols from a MusicXML file instead of grid.txt.",
    )

    return parser.parse_args()


args = parse_args()

if args.musicxml:
    bars = read_musicxml_file(args.musicxml)
    original_grid = format_grid(bars)
    source = args.musicxml
else:
    bars = read_grid_file(args.grid)

    with open(args.grid) as grid:
        original_grid = grid.read()

    source = args.grid

write_markdown_report(bars, "analysis.md", original_grid)
practice_files = write_practice_sheets(bars, "practice_sheets")

print(f"Read {source}")
print("Wrote analysis.md")
print(f"Wrote {len(practice_files)} practice sheets in practice_sheets/")
