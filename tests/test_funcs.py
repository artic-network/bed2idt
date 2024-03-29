import pathlib
import unittest

from bed2idt.main import append_xlsx, chunks


class TestFuncs(unittest.TestCase):
    def test_chunks(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 3
        result = list(chunks(lst, n))
        expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
        self.assertEqual(result, expected)

    def test_append_xlsx(self):
        valid_path = pathlib.Path("fakepath.xlsx")
        invalid_path = pathlib.Path("fakepath")

        # Test valid path
        result_valid_path = append_xlsx(valid_path)
        self.assertEqual(result_valid_path, valid_path)

        # Test invalid path
        result_invalid_path = append_xlsx(invalid_path)
        self.assertEqual(result_invalid_path, invalid_path.with_suffix(".xlsx"))


if __name__ == "__main__":
    unittest.main()
