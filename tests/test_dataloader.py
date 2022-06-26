import unittest

from airmopss import DataLoader
import pandas as pd
import argparse
config = argparse.Namespace()
config.csv_file = "tests/data/test_dataloader.csv"
config.pkl_file='test/data/newsdata_events.pkl'
config.split = "article"
config.labelled_only = "False"
config.labels_file = "tests/data/newsdata_labels.txt"
config.pipeline = 'en_core_web_sm'

csv_file = "tests/data/test_dataloader.csv"

class DataLoaderTestCase(unittest.TestCase):
    df = pd.read_csv(csv_file)
    dl = DataLoader(config)

    def test_loading(self):
        d = self.dl.data
        self.assertEqual(d[0].title, "le titre")

    def test_content_full(self):
        d = self.dl.data
        self.assertEqual(d[0].content_full, "le titre\n\nla description\n\ncontent x\n\nA paragraph\n\nsecond paragraph\n\nlast paragraph")

    def test_content_full_splitted_article(self):
        c = config
        c.split = "article"
        dl = DataLoader(c)
        d = dl.data
        pattern = [(0, 'le titre\n\nla description\n\ncontent x\n\nA paragraph\n\nsecond paragraph\n\nlast paragraph')]
        self.assertEqual(d[0].content_full_splitted, pattern)

    def test_content_full_splitted_paragraph(self):
        c = config
        c.split = "paragraph"
        dl = DataLoader(c)
        d = dl.data
        test_value = d[0].content_full_splitted
        pattern = [(0, 'le titre\n'), (1, '\n'), (2, 'la description\n'), (3, '\n'), (4, 'content x\n'), (5, '\n'), (6, 'A paragraph\n'), (7, '\n'), (8, 'second paragraph\n'), (9, '\n'), (10, 'last paragraph')]
        self.assertEqual(test_value, pattern)

    def test_get_seq(self):
        c = config
        c.split = "paragraph"
        dl = DataLoader(c)
        test_value = dl.get_seq(6, 18)
        pattern = "graph\n\nsecon"
        self.assertEqual(test_value, pattern)


if __name__ == '__main__':
    unittest.main()