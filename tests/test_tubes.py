import pathlib
import unittest
import tempfile
import xlsxwriter
from primalbedtools.scheme import Scheme

from bed2idt.main import tubes_go
from bed2idt.config import TubePurification, TubeScale
import pandas as pd

BED_PATH = pathlib.Path(__file__).parent / "test_input/primer.bed"


class TestTubeWriter(unittest.TestCase):
    def setUp(self) -> None:
        self.scheme = Scheme.from_file(str(BED_PATH))
        return super().setUp()

    def test_write_tubes(self):
        """Write tubes"""

        with tempfile.TemporaryDirectory(dir="tests", suffix="-tube") as tempdir:
            tempdir_path = pathlib.Path(tempdir)
            output = tempdir_path / "output.xlsx"
            workbook = xlsxwriter.Workbook(output)

            scale = TubeScale.NM25
            purification = TubePurification.STD

            # Write the plate
            tubes_go(self.scheme, workbook, scale, purification)

            # Check the plate is as expected
            df = pd.read_excel(output, sheet_name=None)

            pn_to_seq = {bl.primername: bl.sequence for bl in self.scheme.bedlines}
            found_pn = set()

            # Check Sequences match
            for _sheetname, sheet in df.items():
                # Check structure
                self.assertEqual(
                    ["Name", "Sequence", "Scale", "Purification"],
                    sheet.columns.to_list(),
                )
                # Check primernames are present
                for row in sheet.itertuples():
                    # check correct seq is provided
                    self.assertEqual(pn_to_seq[row.Name], row.Sequence)  # type: ignore
                    found_pn.add(row.Name)

                    # Check the Scale and purification
                    self.assertEqual(row.Scale, scale.value)
                    self.assertEqual(row.Purification, purification.value)

            # Check all primers are present
            self.assertSetEqual(found_pn, set(pn_to_seq.keys()))


if __name__ == "__main__":
    unittest.main()
