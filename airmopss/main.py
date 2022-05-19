#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import os
import sys
import spacy
from spacy import displacy
import pandas as pd
import pandas as pd
import numpy as np
import json
from pprint import pprint

import transformers
from transformers import pipeline
from transformers import PegasusTokenizer, PegasusForConditionalGeneration

from airmopss_utils import *
from airmopss_spacy_utils import *
from airmopss_preprocess import *


MAX=1

pipeline = ["tok2vec", "tagger", "parser", "ner"]





def get_elements(doc, dep='nsubj', exclude_pos=['PRON'], include_ner=['GPE', 'PERSON', 'ORG', 'NORP']):
    """
    Displays and returns elements with a specific dependency and filtered on excluded pos and included ner
    :param doc:
    :param dep:
    :param exclude_pos:
    :param include_ner:
    :return:
    """
    elements_list = []
    for word in doc:
        if word.dep_ == dep and word.pos_ not in exclude_pos:
            word_subtree = word.subtree
            flag = False
            for elt in word_subtree:
                flag = flag or elt.ent_type_ in include_ner
            if flag:
                elements_list.append([elt for elt in word.subtree])

    #for elt in elements_list:
    #    print(elt)
    return elements_list

def article(data, num):
    return

def create_ner_module(module_name):
    nlp = spacy.blank("en")

    ner = nlp.create_pipe("ner")

    nlp.add_pipe("ner", name=module_name)

    nlp.to_disk("custom_test_ner")

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
        labelled_art = [101, 102, 105, 107, 108, 120, 125, 127, 129, 134, 137, 142, 145, 151, 156, 160, 172, 180, 188,
                        196,
                        301, 304, 306, 308, 309, 312]

        for i in labelled_art:
            articles.append(df.iloc[i]["content_y"])
            descriptions.append(df.iloc[i]["description"])
            titles.append(df.iloc[i]["title"])

        return [titles, descriptions, articles]

    def get_pipeline(self, pipeline):
        return spacy.load(pipeline)

# print(doc.text)
    # for token in doc:
    #     print(token.text, token.pos_, token.dep_)
    #     if token.dep_ == 'nsubj':
    #         print(token.subtree)


class DataProcessing():
    def __init__(self, config, data_loader):
        self.data = data_loader.data
        self.pipeline = data_loader.pipeline

    def run(self, task="extract_np"):
        if task == "extract_np":
            self._extract_np()
        elif task == "qa":
            self._extract_qa()
        else:
            print(f"No task{task} defined")
            pass

    def _extract_np(self):
        titles, descriptions, articles = self.data
        nlp = self.pipeline

        # loop over all the articles
        num_articles = range(len(articles))
        # num_articles=[0]
        for i in num_articles:
            title = titles[i]
            description = descriptions[i]
            # print(articles[i])
            article = clean_text(articles[i])

            head(title)
            doc = nlp(article)
            print(doc.ents)  # returns doc entities
            print(article)
            print("\n#### SUBJ ####\n")
            subjs = get_elements(doc)
            subjs = tokens_to_list_unique(subjs)
            print("\n".join(subjs))

            print("\n#### DOBJ ####\n")
            dobjs = get_elements(doc, dep='dobj')

            # print(ents[0].ent_iob_) # renvoie O, I, ou B (outside, inside, beginning)
            # displacy.serve(doc, host="localhost", port=5000, style='ent')  # visualisation de la NER
            # displacy.serve(doc, host="localhost", port=5001, style='dep')  # visualisation de la NER

    def _extract_qa(self):
        while True:
            q = input("Enter a question: ")
            if q == "#": break
            print(q)

def main(config):
    # load data
    data_loader = DataLoader(config)

    # process
    data_processor = DataProcessing(config, data_loader)
    data_processor.run()
    data_processor.run(task="summarize")
    data_processor.run(task="qa")

    #create_ner_module("geopolitics_ner")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, default='data/newsdata.csv')
    parser.add_argument('--pipeline', type=str, default='en_core_web_sm')
    config = parser.parse_args()

    main(config)

    # parser.add_argument("--decay_epoch", type=int, default=100, help="epoch from which to start lr decay")
    # parser.add_argument("--n_cpu", type=int, default=8, help="number of cpu threads to use during batch generation")
    # parser.add_argument("--lambda_cyc", type=float, default=10.0, help="cycle loss weight")
    # parser.add_argument('--cuda_parallel', type=str2bool, default=False)
    # parser.add_argument('--epochs', type=int, default=40000, help="number of epochs of training")
    # parser.add_argument('--datasets_path', type=str, default='~/datasets')


    # display diffent kind of labels
    # get_labels("ner")
    # get_labels("tagger")
    # get_labels("parser")
    #print(nlp.disabled)


