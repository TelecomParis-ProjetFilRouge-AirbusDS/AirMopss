import unittest

from airmopss import DataLoader
import pandas as pd
csv_file="tests/data/test_dataloader.csv"

class DataLoaderTestCase(unittest.TestCase):
    def test_loading(self):
        df = pd.read_csv(csv_file)
        idx= df.iloc[0].id
        self.assertEqual(idx, 3)


if __name__ == '__main__':
    unittest.main()