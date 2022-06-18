#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles the DataLoader class
"""

import pandas as pd
import spacy
import json
from .utils import needleman_wunsch
from .preprocessing import *
import re
import logging

#pipelines = ["tok2vec", "tagger", "parser", "ner"]

class DataLoader():
    """
    The class handles the loading of a csv file and functions to manipulate data.

    Supported csv file header :
    "id, author, title, description, url, urlToImage, publishedAt, content_x, source.id, source.name, content_y"

    """
    def __init__(self, config):
        """
        Constructor is initialized using 'config' parameter

        :param config: arguments in a namespace
        """
        logging.info(f"Building {__class__.__name__} instance")

        self.config = config
        self.data = self.load_data(config.csv_file)


        # TODO : to remove before delivery
        if config.debug_mini_load:
            pass
        else:
            # en_core_web_sm ou autre
            self.pipeline = self.get_pipeline(config.spacy_pipeline)

        self.sequences = []

    def load_data(self, csv_file, labelled_only=False):
        """
        Loads content of csv file into a dict. The supported file header which format is:

        "id,author,title,description,url,urlToImage,publishedAt,content_x,source.id,source.name,content_y"

        The dict key is the article 'id' and the values are the header fields.

        Additional fields are created and used:

        * content_full
        * content_clean

        Some fields are experimental:

        * content_paragraphs
        * content_full_splitted

        :param csv_file:
        :param labelled_only: keeps specific labeled articles only (experimental)
        :return: a dictionnary of articles (key as id)
        """
        logging.debug("Loading data")
        df = pd.read_csv(csv_file)

        # convert to a dictionary
        d = df.transpose().to_dict(orient='series')

        for k, v in d.items():
            _t = str(d[k]["title"])
            _d = str(d[k]["description"])
            _x = str(d[k]["content_x"])
            _y = str(d[k]["content_y"])
            d[k]["content_full"] = _t+"\n\n"+_d+"\n\n"+_y
            d[k]["content_clean"] = self.load_data_preprocess(_t, _d, _x, _y)
            # TODO à réanalyser
            d[k]["content_paragraphs"] = [line for line in self._split_into_paragraph(d[k]["content_clean"][1])]

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

        if labelled_only:
            art_ids = [101, 102, 105, 107, 108, 120, 125, 127, 129, 134, 137, 142, 145, 151, 156, 160, 172, 180, 188, 196, 301, 304, 306, 308, 309, 312]
        else:
            # TODO check len(df) matched art ids if needed
            art_ids = range(len(df))

        # TODO remove the complement instead
        for idx in art_ids:
            #d.pop(idx, None)
            pass

        logging.debug("Data loaded")

        return d



    def get_aligned_indices(self, text_original, text_clean):
        """
        Returns a dict of key/value pairs of indices over two strin sequences.

        The key is the index in the preprocessed sequence and the value is the index in the original sequence

        Example:

        * original sequence: CAT
        * sequence to align: CT
        * output : {1: 1}

        :param id_article:
        :return: dict
        """
        _d = {elt[1]: elt[0] for elt in needleman_wunsch(text_original, text_clean) if elt[0] is not None and elt[1] is not None}
        return _d

    def get_aligned_indices_article(self, id_article):
        """
        Returns a dict of key/value pairs over the 'content_full' and 'content_clean' fields of the article with id 'id_article'

        The key is the index in the preprocessed sequence and the value is the index in the original sequence

        Example:

        * original sequence: CAT
        * sequence to align: CT
        * output : {1: 1}

        :param id_article:
        :return: dict
        """

        # On récupère une liste d'indices, on veut juste les traduire.
        _text_original = self.data[id_article]["content_full"]
        _text_clean = self.data[id_article]["content_clean"]

        _d = {elt[1]: elt[0] for elt in needleman_wunsch(_text_original, _text_clean) if elt[0] is not None and elt[1] is not None}
        return _d

    def _split_into_paragraph(self, content):
        """
        Returns a list that contains a splitted version of the string 'content'

        :param content:
        :return:
        """
        return content.splitlines(True)

    def _split_into_sentence(self, content):
        """
        :param content:
        :return:
        """
        # TODO
        return content.split(".!?")

    # getters
    def get_data_author(self, idx):
        """
        Returns the 'author' field of article idx

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["author"]

    def get_data_title(self, idx):
        """
        Returns the 'title' field of article idx

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["title"]

    def get_data_description(self, idx):
        """
        Returns the 'description' field of article idx

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["description"]

    def get_data_url(self, idx):
        """
        Returns the 'url' field of article idx

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["url"]

    def get_data_urlToImage(self, idx):
        """
        Returns the 'urlToImage' field of article idx

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["urlToImage"]

    def get_data_publishedAt(self, idx):
        """
        Returns the 'publishedAt' field of article idx

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["publishedAt"]

    def get_data_content_x(self, idx):
        """
        Returns the 'content_x' field of article idx

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["content_x"]

    def get_data_source_id(self, idx):
        """
        Returns the 'surce_id' field of article idx

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["source.id"]

    def get_data_source_name(self, idx):
        """
        Returns the 'source_name' field of article idx

        Ex: BBC, Reuters

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["source.name"]

    def get_data_content_y(self, idx):
        """
        Returns the 'content_y' field of article idx which is the main body of the article

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["content_y"]

    def get_data_content_full(self, idx):
        """
        Returns the 'content_full' field of article idx which contains the title, description, content_y

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["content_full"]

    def get_data_content_clean(self, idx):
        """
        Returns the 'content_clean' field of article idx which contains the cleaned **preprocessed content** of the article

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["content_clean"]

    def get_data_content_paragraphs(self, idx):

        """
        Returns the 'content_paragraphs' field of article idx

        (Feature on development)

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["content_paragraphs"]

    def get_data_content_full_splitted(self, idx):
        """
        Returns the 'full_splitted' field of article idx

        Experimental

        :param idx: id of the article
        :return:
        """
        return self.data[idx]["content_full_splitted"]

    def get_seq(self, id_start, id_end, id_article=0, field='content_y' ):
        t = self.data[id_article][field]
        if id_start < id_end < len(t):
            return t[id_start:id_end]
        else:
            return t

    def load_data_preprocess(self, title, description, content_x, content_y):
        """
        Preprocess the content of an article based on specific csv file fields

        :param title: the title
        :param description: the description
        :param content_x: a short description
        :param content_y: the main content
        :return: a tuple containing a list of paragraphs and the preprocessed article
        """
        start = content_y.find(content_x[:50])
        if start != -1:
            content_y = content_y[start:]

        _cleaned_content = clean_text(content_y)

        article = title + "\n\n" + description + "\n\n" + _cleaned_content

        # TODO : use split_paragraphs() function instead
        clean_article_regex = re.sub("\n\S+\n\n+", "\n", article)
        clean_article_regex = re.sub("\n+", "\n", clean_article_regex)
        paragraphs = clean_article_regex.split('\n')
        paragraphs = [paragraph for paragraph in paragraphs]
        return paragraphs, article

    def load_labels(self, json_file):
        """
        Opens JSON file of labels

        :param json_file: file contains annotated articles
        :return:
        """
        with open(json_file) as f:
            data = json.load(f)
        return data

    def get_pipeline(self, pipeline):
        """
        Loads and returns the Spacy transformer-based pipeline

        :param pipeline: name of the pipeline to use
        :return: a pipeline instance
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
    output = dl._split_into_paragraph("A paragraph\n\nsecond paragraph\n\nlast paragraph")
    output = dl.get_aligned_indices(0)
    print(output)
