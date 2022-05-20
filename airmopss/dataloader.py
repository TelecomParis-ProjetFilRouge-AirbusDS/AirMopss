#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import spacy

#pipelines = ["tok2vec", "tagger", "parser", "ner"]

class DataLoader():
    def __init__(self, config):

        self.data = self.get_data(config.csv_file)
        self.pipeline = self.get_pipeline(config.pipeline)

    def get_data(self, csv_file):
        """
        Returns a tuple of titles, descriptions, articles from csv file
        :param csv_file:
        :return:
        """
        articles = []
        descriptions = []
        titles = []

        df = pd.read_csv(csv_file)
        labelled_art = [101, 102, 105, 107, 108, 120, 125, 127, 129, 134, 137, 142, 145, 151, 156, 160, 172, 180, 188, 196, 301, 304, 306, 308, 309, 312]

        for i in labelled_art:
            articles.append(df.iloc[i]["content_y"])
            descriptions.append(df.iloc[i]["description"])
            titles.append(df.iloc[i]["title"])

        return [titles, descriptions, articles]

    def get_pipeline(self, pipeline):
        return spacy.load(pipeline)