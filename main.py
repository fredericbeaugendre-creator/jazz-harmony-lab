from harmony import read_grid, write_markdown_report, write_practice_sheets

with open("grid.txt") as grid:
    original_grid = grid.read()

bars = read_grid("grid.txt")
write_markdown_report(bars, "analysis.md", original_grid)
practice_files = write_practice_sheets(bars, "practice_sheets")

print("Wrote analysis.md")
print(f"Wrote {len(practice_files)} practice sheets in practice_sheets/")
