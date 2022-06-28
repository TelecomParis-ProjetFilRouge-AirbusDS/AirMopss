#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles the DataProcessing class
"""

from .qaprocessing import QaProcessing
from .dataloader import DataLoader
from .preprocessing import *
from .spacy_utils import *
from .utils import *
import logging

class DataProcessing():
    """
    The class is a handler to launch tasks.
    """
    def __init__(self, config, data_loader: DataLoader, logger=None):
        """
        Constructor is initialized using 'config' parameter and a DataLoader

        :param config: arguments in a namespace
        :param data_loader:
        """
        if logger == None:
            self.logger = logging
        else:
            self.logger = logger

        self.logger.info(f"Building {__class__.__name__} instance")

        self.config = config
        self.data = data_loader.data
        self.data_loader = data_loader

        # TODO : to remove before delivery
        if config.debug_mini_load:
            pass
        else:
            self.pipeline = data_loader.pipeline

        #if "qa" == config.task:
        self.qa = QaProcessing(config, data_loader)

    def run(self, task="extract_np"):
        """
        Launches processing based on the 'task' parameter.

        The default task is passed though the `config.task` parameter.

        :return: None
        """
        if task == "extract_np":
            self._extract_np()

        elif task == "qa":
            self.qa.process()

        elif task == "generate_pickle":
            self.qa.process_and_store()

        elif task == "version":
            print("Versions:")
            print("Spacy", spacy.__version__)
        else:
            print(f"No <{task}> task defined")
            pass

    def get_elements(self, doc, dep='nsubj', exclude_pos=['PRON'], include_ner=['GPE', 'PERSON', 'ORG', 'NORP']):
        """
        Returns a list of elements with the specific dependency 'dep'.
        The elements are filtered and limited to one that exclude parts of speech 'exclude_pos'
        and that contain at least one named named entity among 'include_ner'.

        # TODO detailed the element structure

        :param doc: the text to match on
        :param dep: the dependency to match on
        :param exclude_pos: the excluded parts of speech
        :param include_ner: a must have named entity
        :return: a list of patterns matching the dependency
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

        return elements_list


    def _extract_np(self):
        """

        :return:
        """
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
            subjs = self.get_elements(doc)
            subjs = tokens_to_list_unique(subjs)
            print("\n".join(subjs))

            print("\n#### DOBJ ####\n")
            dobjs = self.get_elements(doc, dep='dobj')


    def score_func(self, gt, pred):
        """
        Computes the F1 score

        # TODO what are gt and pred, rename variables
        :param gt:
        :param pred:
        :return: the computed F1 score
        """
        TP = len(gt.intersection(pred))
        FN = len(gt - pred)
        FP = len(pred - gt)

        # Calcul du score F1
        if (TP+FP)*(TP+FN)*TP != 0:
            precision = TP/(TP+FP)
            recall = TP/(TP+FN)
            F1 = 2 * precision * recall / (precision + recall)
        else :
            F1 = 1

        return F1
