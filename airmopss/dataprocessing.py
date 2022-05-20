#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocess import *
from spacy_utils import *

class DataProcessing():
    def __init__(self, config, data_loader):
        self.data = data_loader.data
        self.pipeline = data_loader.pipeline

    def run(self, task="extract_np"):
        if task == "extract_np":
            self._extract_np()
        elif task == "qa":
            self._extract_qa()
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

    def _extract_qa(self):
        while True:
            q = input("Enter a question: ")
            if q == "#": break
            print(q)