import os
import tempfile
import unittest

from harmony import (
    chord_tones,
    common_notes,
    detect_secondary_dominants,
    infer_reference_key,
    important_tones,
    parse_chord_symbol,
    scale_notes,
    suggested_scales,
)
from importers import read_grid_file, read_musicxml_file


class HarmonyTests(unittest.TestCase):
    def test_chord_tones_use_musical_spelling(self):
        self.assertEqual(chord_tones("Gmaj7"), ["G", "B", "D", "F#"])
        self.assertEqual(chord_tones("F#maj7"), ["F#", "A#", "C#", "E#"])

    def test_scale_notes_use_musical_spelling(self):
        self.assertEqual(scale_notes("G", "Ionian"), ["G", "A", "B", "C", "D", "E", "F#"])
        self.assertEqual(scale_notes("C", "Lydian"), ["C", "D", "E", "F#", "G", "A", "B"])

    def test_common_notes_match_enharmonic_equivalents(self):
        self.assertEqual(common_notes(["F#"], ["Gb", "A"]), ["F#"])

    def test_slash_chords_parse_and_analyse_from_their_root(self):
        self.assertEqual(parse_chord_symbol("Cmaj7/E"), ("C", "maj7"))
        self.assertEqual(chord_tones("Cmaj7/E"), ["C", "E", "G", "B"])

    def test_extended_chord_qualities(self):
        self.assertEqual(chord_tones("CmMaj7"), ["C", "Eb", "G", "B"])
        self.assertEqual(chord_tones("C7#11"), ["C", "E", "G", "Bb", "F#"])
        self.assertEqual(chord_tones("C7sus"), ["C", "F", "G", "Bb"])
        self.assertIn("C altered", suggested_scales("Calt"))
        self.assertEqual(important_tones("Cadd9"), ["3rd: E", "9th: D"])
        self.assertEqual(important_tones("C7sus4"), ["4th: F", "7th: Bb"])

    def test_secondary_dominants_use_inferred_reference_key(self):
        chords = ["Gmaj7", "E7", "Am7", "D7", "Gmaj7"]
        movements = detect_secondary_dominants(chords)

        self.assertEqual(infer_reference_key(chords), "G")
        self.assertEqual(movements[0]["label"], "V/ii")
        self.assertIn("in G as the inferred reference key", movements[0]["explanation"])


class ImporterTests(unittest.TestCase):
    def test_read_grid_file(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as grid:
            grid.write("| Dm7 G7 | Cmaj7 |\n")
            filename = grid.name

        try:
            self.assertEqual(read_grid_file(filename), [["Dm7", "G7"], ["Cmaj7"]])
        finally:
            os.unlink(filename)

    def test_musicxml_import_normalizes_added_degrees_and_bass(self):
        musicxml = """<?xml version="1.0" encoding="UTF-8"?>
<score-partwise version="3.1">
  <part>
    <measure number="1">
      <harmony>
        <root>
          <root-step>C</root-step>
        </root>
        <kind>major</kind>
        <degree>
          <degree-value>9</degree-value>
          <degree-alter>0</degree-alter>
          <degree-type>add</degree-type>
        </degree>
        <bass>
          <bass-step>E</bass-step>
        </bass>
      </harmony>
    </measure>
    <measure number="2">
      <harmony>
        <root>
          <root-step>G</root-step>
        </root>
        <kind>dominant</kind>
        <degree>
          <degree-value>9</degree-value>
          <degree-alter>-1</degree-alter>
          <degree-type>add</degree-type>
        </degree>
      </harmony>
    </measure>
  </part>
</score-partwise>
"""
        with tempfile.NamedTemporaryFile("w", suffix=".musicxml", delete=False) as chart:
            chart.write(musicxml)
            filename = chart.name

        try:
            self.assertEqual(read_musicxml_file(filename), [["Cadd9/E"], ["G7b9"]])
            self.assertEqual(chord_tones("Cadd9/E"), ["C", "E", "G", "D"])
        finally:
            os.unlink(filename)


if __name__ == "__main__":
    unittest.main()
