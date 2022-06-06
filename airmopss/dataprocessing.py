#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the data processing class of our project.
"""

from .qaprocessing import QaProcessing
from .dataloader import DataLoader
from .preprocessing import *
from .spacy_utils import *
from .utils import *

class DataProcessing():
    """
    This class **is** the application. It contains everything related to the interface, and the core logic of the project.
    """
    def __init__(self, config, data_loader: DataLoader):
        """
        Class initialization
        """
        self.config = config
        self.data = data_loader.data
        self.data_loader = data_loader
        self.pipeline = data_loader.pipeline

        if "qa" == config.task:
            self.qa = QaProcessing(config, data_loader)

    def run(self, task="extract_np"):
        """
        App launch, with main window and everything. Vroum vroum

        :return:
        """
        if task == "extract_np":
            self._extract_np()

        elif task == "qa":
            self.qa.process()

        elif task == "version":
            print("Versions:")
            print("Spacy", spacy.__version__)
        else:
            print(f"No <{task}> task defined")
            pass

    def get_elements(self, doc, dep='nsubj', exclude_pos=['PRON'], include_ner=['GPE', 'PERSON', 'ORG', 'NORP']):
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

        # for elt in elements_list:
        #    print(elt)
        return elements_list

    def _extract_np(self):
        """

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

            # print(ents[0].ent_iob_) # renvoie O, I, ou B (outside, inside, beginning)
            # displacy.serve(doc, host="localhost", port=5000, style='ent')  # visualisation de la NER
            # displacy.serve(doc, host="localhost", port=5001, style='dep')  # visualisation de la NER



    def prepocess(self):
        """

        """
        # TODO un objet DataLoader comporte
        # * data
        # split en
        # * sequences{id_seq et sequence} (article complet, paragraphes ou sentences)
        #
        pass

    def score_func(self, gt, pred):
        """
        Calcul des faux positifs, vrais positifs, faux négatifs

        :param gt: sets
        :param pred: sets
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
