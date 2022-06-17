#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Question Answering processing class
"""
from .preprocessing import *
from .spacy_utils import *
from .utils import *
from .dataloader import DataLoader

import re
from transformers import pipeline
import logging

class QaProcessing():
    """
    Class QaProcessing
    """

    def __init__(self, config, data_loader: DataLoader):
        """
        Constructor

        :param config:
        :param data_loader:
        """
        logging.info(f"Building {__class__.__name__} instance")

        self.data_loader = data_loader

        self.spacy_pipeline = data_loader.pipeline
        self.qa_pipeline = pipeline("question-answering")  # , model="distilbert-base-cased-distilled-squad", tokenizer="bert-base-cased")

        self.questions = self.set_questions()

    def set_questions(self):
        """
        Suite de patterns de questions

        :return:
        """
        questions = [
            "What happened to _GN_?",
            #"What happens to _GN_?",

            #"What did _GN_ do?",
            #"What do _GN_ do?",

            "When did _GN_ _action_?",
            #"When do _GN_ _action_?",
            # "When did _action_ happen?",

            "Where did _GN_ _action_?",
           # "Where do _GN_ _action_?",
            # "Where did _action_ take place?"
        ]
        return questions

    def ask_question(self):
        """

        """
        while True:
            q = input("Enter a question: ")
            if q == "#": break
            print(q)


    # TODO : include Dictionnaire de mapping (dct_mapping) entre articles de base "articles[X]" et article nettoyé doc.text
    def get_gn_subjs(self, doc, increment=0):
        """
        Extraire l'ensemble des groupes nominaux sujets (non-pronominaux) qui sont des entités ['GPE', 'PERSON', 'ORG', 'NORP'] et les index de début et de fin

        ICIC ON DECRIT DCE QUON RENVIE

        :param doc:
        :return:
        """
        np_list_subj = []
        gn_subj_idx = []
        for word in doc:
            if word.dep_ == 'nsubj' and word.pos_ not in ['PRON']:
                word_subtree = word.subtree
                flag = False
                for elt in word_subtree:
                    flag = flag or elt.ent_type_ in ['GPE', 'PERSON', 'ORG', 'NORP']
                if flag:
                    np_list_subj.append([elt for elt in word.subtree])
                    word_index = [elt.idx for elt in word.subtree]
                    word_len = [len(elt) for elt in word.subtree]
                    idx = [word_index[0], word_index[-1] + word_len[-1]]
                    gn_subj_idx.append(idx)

        # reconcatene en liste de string
        gn_subj = [" ".join([str(elt) for elt in GN]).strip() for GN in np_list_subj]
        gn_subj = list(dict.fromkeys(gn_subj))

        return gn_subj, gn_subj_idx

    def preprocess(self, idx):
        """

        :param idx:
        :return:
        """

        #article = self.df.iloc[idx].content_y
        article = self.data_loader.get_data_content_full(idx) # retrun tilte, descr, contents...
        _content_x =  self.data_loader.get_data_content_x(idx)
        _content_y =  self.data_loader.get_data_content_y(idx)
        _, article_splitted = self.data_loader.get_data_content_full_splitted(idx)[0]

        # UGLY below, splittnig partially done on data_loader
        article = clean_text(article)

        # start = self.df.iloc[idx].content_y.find(self.df.iloc[idx].content_x[:50])
        start = _content_y.find(_content_x[:50])

        if start != -1:
            article = article[start:]

        # TODO : the following would need to be included in preprocessing.py
        clean_article_regex = re.sub("\n\S+\n\n+", "\n", article)
        clean_article_regex = re.sub("\n+", "\n", clean_article_regex)
        paragraphs = clean_article_regex.split('\n')
        paragraphs = [paragraph for paragraph in paragraphs if (len(paragraph.split(' ')) > 10
                                                                and "Show caption" not in paragraph
                                                                and "Getty images" not in paragraph
                                                                and "@" not in paragraph)]
        return paragraphs, article

    # TODO : complete function
    def process_raw_txt(self, input_txt):
        """

        :param input_txt:
        :return:
        """
        # TODO change idx to sth else
        paragraphs, article = self.preprocess_txt(input_txt)

        list = []
        for i, word in enumerate(input_txt.split()):
            if 'b' in word:
                list.append(i)
        return list

    def process(self):
        """

        :return:
        """
        #articles = self.data[2]
        # TODO : to extend or fix depending on desired process
        for idx in [101]:

            #clean_article_regex = re.sub("\n\S+\n\n+", "\n", articles[idx])
            #clean_article_regex = re.sub("\n+", "\n", clean_article_regex)

            paragraphs, article = self.preprocess(idx)

            answers_all = []
            for paragraph in paragraphs:

                #print(paragraph, end='\n\n')

                doc = self.spacy_pipeline(paragraph)

                gn_subj, gn_subj_idx = self.get_gn_subjs(doc, increment=0)

                print("*"*30, "\n", "Paragraph:" , doc, '\n')

                for GN in gn_subj:

                    scores = {'what': 5e-3, 'who': 5e-3, 'when': 5e-2, 'where': 5e-2}
                    # preds = {'what':None, 'who':None, 'when':None, 'where':None}
                    preds = {'what': "XXX", 'who': GN, 'when': "XXX", 'where': "XXX"}

                    answers_gn = []

                    for idx, question in enumerate(self.questions):

                        question = question.replace("_GN_", GN)
                        qu = question.split()[0].lower()
                        if qu != "what":
                            question = question.replace("_action_", preds['what'])

                        result = self.qa_pipeline(question=question, context=paragraph)
                        answer = result['answer']
                        score = result['score']

                        answers_gn.append(answer)

                        if score > scores[qu]:
                            preds[qu] = answer
                            scores[qu] = score
                        else:
                            print("Score too low")

                        print(question, ' : ', answer, ' score : ', score)

                    answers_all.append(answers_gn)

                    # display([ key + ": " + preds[key] + " (" + str(scores[key]) + ")"  for key in preds.keys()])
                    print('\n')

        print(answers_all)

        return answers_all