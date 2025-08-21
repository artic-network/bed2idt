import pathlib
import unittest
import tempfile
import xlsxwriter
from primalbedtools.scheme import Scheme

from bed2idt.main import plates_go
from bed2idt.config import PlateSplitBy, PlateFillBy, PlateSize

import pandas as pd

BED_PATH = pathlib.Path(__file__).parent / "test_input/primer.bed"


class TestPlateWriter(unittest.TestCase):
    def setUp(self) -> None:
        self.scheme = Scheme.from_file(str(BED_PATH))
        return super().setUp()

    def test_write_96(self):
        """Write a 96 well plate"""

        with tempfile.TemporaryDirectory(
            dir="tests", suffix="-96well-plate"
        ) as tempdir:
            tempdir_path = pathlib.Path(tempdir)
            output = tempdir_path / "output.xlsx"
            workbook = xlsxwriter.Workbook(output)

            # Write the plate
            plates_go(
                self.scheme,
                workbook,
                PlateSplitBy.REF,
                PlateFillBy.ROWS,
                "test",
                False,
                PlateSize.WELL96,
            )

            # Check the plate is as expected
            df = pd.read_excel(output, sheet_name=None)

            pn_to_seq = {bl.primername: bl.sequence for bl in self.scheme.bedlines}
            found_pn = set()

            sheet_names = []
            # Check Sequences match
            for _sheetname, sheet in df.items():
                # Check structure
                self.assertEqual(
                    ["Well Position", "Name", "Sequence"], sheet.columns.to_list()
                )
                # Check primernames are present
                for row in sheet.itertuples():
                    # check correct seq is provided
                    self.assertEqual(pn_to_seq[row.Name], row.Sequence)  # type: ignore
                    found_pn.add(row.Name)

                sheet_names.append(_sheetname)

            # Check all primers are present
            self.assertSetEqual(found_pn, set(pn_to_seq.keys()))
            # Check all sheet names are present
            self.assertEqual(sheet_names, ["test_MN908947.3.0", "test_MN908947.3.1"])

    def test_write_96_split_ref_pool(self):
        """Write a 96 well plate"""

        with tempfile.TemporaryDirectory(
            dir="tests", suffix="-96well-plate"
        ) as tempdir:
            tempdir_path = pathlib.Path(tempdir)
            output = tempdir_path / "output.xlsx"
            workbook = xlsxwriter.Workbook(output)

            # Write the plate
            plates_go(
                self.scheme,
                workbook,
                PlateSplitBy.REF_POOL,
                PlateFillBy.ROWS,
                "test",
                False,
                PlateSize.WELL96,
            )

            # Check the plate is as expected
            df = pd.read_excel(output, sheet_name=None)

            pn_to_seq = {bl.primername: bl.sequence for bl in self.scheme.bedlines}
            found_pn = set()

            sheet_names = []
            # Check Sequences match
            for _sheetname, sheet in df.items():
                # Check structure
                self.assertEqual(
                    ["Well Position", "Name", "Sequence"], sheet.columns.to_list()
                )
                # Check primernames are present
                for row in sheet.itertuples():
                    # check correct seq is provided
                    self.assertEqual(pn_to_seq[row.Name], row.Sequence)  # type: ignore
                    found_pn.add(row.Name)

                sheet_names.append(_sheetname)

            # Check all primers are present
            self.assertSetEqual(found_pn, set(pn_to_seq.keys()))
            # Check all sheet names are present
            self.assertEqual(
                sheet_names, ["test_MN908947.3_1.0", "test_MN908947.3_2.0"]
            )

    def test_write_384(self):
        """Write a 384 well plate"""

        with tempfile.TemporaryDirectory(
            dir="tests", suffix="-384well-plate"
        ) as tempdir:
            tempdir_path = pathlib.Path(tempdir)
            output = tempdir_path / "output.xlsx"
            workbook = xlsxwriter.Workbook(output)

            # Write the plate
            plates_go(
                self.scheme,
                workbook,
                PlateSplitBy.POOL,
                PlateFillBy.ROWS,
                "test",
                False,
                PlateSize.WELL384,
            )

            # Check the plate is as expected
            df = pd.read_excel(output, sheet_name=None)

            pn_to_seq = {bl.primername: bl.sequence for bl in self.scheme.bedlines}
            found_pn = set()

            sheet_names = []
            # Check Sequences match
            for _sheetname, sheet in df.items():
                # Check structure
                self.assertEqual(
                    ["Well Position", "Name", "Sequence"], sheet.columns.to_list()
                )
                # Check primernames are present
                for row in sheet.itertuples():
                    # check correct seq is provided
                    self.assertEqual(pn_to_seq[row.Name], row.Sequence)  # type: ignore
                    found_pn.add(row.Name)
                sheet_names.append(_sheetname)

            # Check all primers are present
            self.assertSetEqual(found_pn, set(pn_to_seq.keys()))

            # Check all sheet names are present
            self.assertEqual(sheet_names, ["test_1.0", "test_2.0"])


if __name__ == "__main__":
    unittest.main()
