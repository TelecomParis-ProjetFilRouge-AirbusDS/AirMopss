#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import spacy
import json

#pipelines = ["tok2vec", "tagger", "parser", "ner"]

class DataLoader():
    """
    Load data from a csv file

    Fields available in csv file :
    id, author, title, description, url, urlToImage, publishedAt, content_x, source.id, source.name, content_y

    """
    def __init__(self, config):
        """

        :param config:
        """
        self.config = config

        self.data = self.load_data(config.csv_file)

        self.pipeline = self.get_pipeline(config.pipeline)

    def load_data(self, csv_file, labelled_only=False):
        """
        Loads content of csv file into a dict

        :param csv_file:
        :param labelled_only:
        :return:
        """

        df = pd.read_csv(csv_file)

        #d = df.set_index('id').T.to_dict('list')
        d = df.transpose().to_dict(orient='series')

        for k, v in d.items():
            _t = str(d[k]["title"])
            _d = str(d[k]["description"])
            _x = str(d[k]["content_x"])
            _y = str(d[k]["content_y"])
            d[k]["content_full"] = _t+"\n\n"+_d+"\n\n"+_x+"\n\n"+_y

        # TODO handle split into paragraph, sentence
        _split = []
        if self.config.split == 'article':
            for k, v in d.items():
                _split = [(0, d[k]["content_full"])]
                d[k]["content_full_splitted"] = _split


        elif self.config.split == 'paragraph':
            for k, v in d.items():
                _split = [(idx, line) for idx, line in enumerate(self._split_into_paragraph(d[k]["content_full"]))]
                d[k]["content_full_splitted"] = _split

        elif self.config.split == 'sentence':
            for k, v in d.items():
                _split = [(idx, line) for idx, line in enumerate(self._split_into_sentence(d[k]["content_full"]))]
                d[k]["content_full_splitted"] = _split

        else:
            for k, v in d.items():
                _split = [(0, d[k]["content_y"])]
                d[k]["content_full_splitted"] = _split

        return d

        # if labelled_only:
        #     art_ids = [101, 102, 105, 107, 108, 120, 125, 127, 129, 134, 137, 142, 145, 151, 156, 160, 172, 180, 188, 196, 301, 304, 306, 308, 309, 312]
        # else:
        #     # TODO check len(df) matched art ids if needed
        #     art_ids = range(len(df))
        #
        # # TODO remove the complement instead
        # for idx in art_ids:
        #     d.pop(idx, None)

        for idx in art_ids:
            articles.append(df.iloc[idx]["content_y"])
            descriptions.append(df.iloc[idx]["description"])
            titles.append(df.iloc[idx]["title"])

    def _split_into_paragraph(self, content):
        return content.splitlines(True)

    def _split_into_sentence(self, content):
        # TODO
        return content.split(".!?")

        return [titles, descriptions, articles]

    def load_labels(self, json_file):
        """
        Opens JSON file of labels

        :param json_file:
        :return:
        """
        with open(json_file) as f:
            data = json.load(f)
        return data

    def get_pipeline(self, pipeline):
        """

        :param pipeline:
        :return:
        """
        return spacy.load(pipeline)if __name__ == '__main__':

if __name__ == '__main__':
    import argparse
    config = argparse.Namespace()
    config.csv_file = "../tests/data/test_dataloader.csv"
    config.split = "paragraph"
    config.labelled_only = "False"
    config.pipeline = 'en_core_web_sm'

    dl = DataLoader(config)
    dl.load_data(config.csv_file)