#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import spacy
import json
from utils import needleman_wunsch

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
        self.sequences = []

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
            d[k]["content_full"] = _t+"\n\n"+_d+"\n\n"+_y
            d[k]["content_clean"] = self.preprocess(d[k]["content_full"])

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

    def get_aligned_indices(self, id_article):
        """
        Return a dict of key values.
        The key is the index in the preprocessed sequence and the value is the the index of the original sequence

        CAT - CT
        {1: 1}

        :param id_article:
        :return: dict
        """

        # On récupère une liste d'indices, on veut juste les traduire.
        _text_original = self.data[id_article]["content_full"]
        _text_clean = self.data[id_article]["content_clean"]

        _d = {elt[1]: elt[0] for elt in needleman_wunsch(_text_original, _text_clean) if elt[0] is not None and elt[1] is not None}
        return _d


    def _split_into_paragraph(self, content):
        return content.splitlines(True)

    def _split_into_sentence(self, content):
        # TODO
        return content.split(".!?")

    # getters
    def get_data_author(self, idx):
        return self.data[idx]["author"]

    def get_data_title(self, idx):
        return self.data[idx]["title"]

    def get_data_description(self, idx):
        return self.data[idx]["description"]

    def get_data_url(self, idx):
        return self.data[idx]["url"]

    def get_data_urlToImage(self, idx):
        return self.data[idx]["urlToImage"]

    def get_data_publishedAt(self, idx):
        return self.data[idx]["publishedAt"]

    def get_data_content_x(self, idx):
        return self.data[idx]["content_x"]

    def get_data_source_id(self, idx):
        return self.data[idx]["source.id"]

    def get_data_source_name(self, idx):
        return self.data[idx]["source.name"]

    def get_data_content_y(self, idx):
        return self.data[idx]["content_y"]

    def get_data_content_full(self, idx):
        """
        returns field containing concat of title, description, content_x, content_y
        """
        return self.data[idx]["content_full"]

    def get_data_content_full_splitted(self, idx):
        """
        returns field containing concat of title, description, content_x, content_y splitted in article, paragraph or sentence
        """
        return self.data[idx]["content_full_splitted"]

    def get_seq(self, id_start, id_end, id_article=0, field='content_y' ):
        t = self.data[id_article][field]
        if id_start < id_end < len(t):
            return t[id_start:id_end]
        else:
            return t

    def preprocess(self, txt):
        return txt

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
        return spacy.load(pipeline)

if __name__ == '__main__':
    import argparse
    config = argparse.Namespace()
    config.csv_file = "../tests/data/test_dataloader.csv"
    config.split = "paragraph"
    config.labelled_only = "False"
    config.pipeline = 'en_core_web_sm'

    dl = DataLoader(config)
    dl.load_data(config.csv_file)
    #print(dl._split_into_paragraph("A paragraph\n\nsecond paragraph\n\nlast paragraph"))
    output = dl.get_aligned_indices(0)
    print(output)
