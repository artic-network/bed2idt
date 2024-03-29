import pathlib
import unittest

from bed2idt.main import read_bedfile


class TestBedFile(unittest.TestCase):
    def setUp(self) -> None:
        self.bedfile = pathlib.Path("tests/test_input/primer.bed")

    def test_read_bedfile(self):
        header, primers = read_bedfile(self.bedfile)

        # Check correct length
        self.assertEqual(len(primers), 192)

        # Check correct header
        self.assertEqual(header, [])

        # Check correct primer ref
        self.assertEqual(primers[0][0], "MN908947.3")
