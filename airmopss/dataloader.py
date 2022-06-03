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

        self.data = self.load_data(config.csv_file, config.labelled_only)
        self.labels = self.load_labels(config.labels_file)
        self.pipeline = self.get_pipeline(config.pipeline)

    def load_data(self, csv_file, labelled_only):
        """
        Returns a tuple of titles, descriptions, articles from csv file
        :param csv_file:
        :return:
        """
        articles = []
        descriptions = []
        titles = []

        df = pd.read_csv(csv_file)

        if labelled_only:
            art_ids = [101, 102, 105, 107, 108, 120, 125, 127, 129, 134, 137, 142, 145, 151, 156, 160, 172, 180, 188, 196, 301, 304, 306, 308, 309, 312]
        else:
            # TODO check len(df) matched art ids if needed
            art_ids = range(len(df))

        for idx in art_ids:
            articles.append(df.iloc[idx]["content_y"])
            descriptions.append(df.iloc[idx]["description"])
            titles.append(df.iloc[idx]["title"])

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
        return spacy.load(pipeline)