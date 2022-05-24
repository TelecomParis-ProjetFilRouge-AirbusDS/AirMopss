#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocessing import *
from spacy_utils import *
import re

import transformers
from transformers import pipeline


class QaProcessing():
    def __init__(self, config, data_loader):
        self.data = data_loader.data
        self.pipeline = data_loader.pipeline
        self.qa_pipeline = pipeline("question-answering")  # , model="distilbert-base-cased-distilled-squad", tokenizer="bert-base-cased")

        self.questions = self.set_questions()

    def set_questions(self):
        # Pipeline de questions
        questions = [
            "What happened to _GN_?",
            "What happens to _GN_?",

            "What did _GN_ do?",
            "What do _GN_ do?",

            "When did _GN_ _action_?",
            "When do _GN_ _action_?",
            # "When did _action_ happen?",

            "Where did _GN_ _action_?",
            "Where do _GN_ _action_?",
            # "Where did _action_ take place?"
        ]
        return questions

    def ask_question(self):
        while True:
            q = input("Enter a question: ")
            if q == "#": break
            print(q)

    def process(self):
        articles = self.data[2]

        for idx in [0]:
            clean_article_regex = re.sub("\n\S+\n\n+", "\n", articles[idx])
            clean_article_regex = re.sub("\n+", "\n", clean_article_regex)

            doc = self.pipeline(clean_article_regex)
            deps = [word.dep_ for word in doc]  # extrait les dépendances entre les entités
            ents = list(doc.ents)  # doc.ents extrait les entités nommées

            # Extraire l'ensemble des groupes nominaux et qui soient dans ['GPE', 'PERSON', 'ORG', 'NORP']
            np_list_subj = []
            for word in doc:
                if word.dep_ == 'nsubj' and word.pos_ not in ['PRON']:
                    word_subtree = word.subtree
                    flag = False
                    for elt in word_subtree:
                        flag = flag or elt.ent_type_ in ['GPE', 'PERSON', 'ORG', 'NORP']
                    if flag:
                        np_list_subj.append([elt for elt in word.subtree])


            print(doc, '\n')

            gn_subj = [" ".join([str(elt) for elt in GN]).strip() for GN in np_list_subj]
            gn_subj = list(dict.fromkeys(gn_subj))

            for GN in gn_subj:

                scores = {'what': 5e-3, 'who': 5e-3, 'when': 5e-2, 'where': 5e-2}
                # preds = {'what':None, 'who':None, 'when':None, 'where':None}
                preds = {'what': "XXX", 'who': GN, 'when': "XXX", 'where': "XXX"}

                for idx, question in enumerate(self.questions):

                    question = question.replace("_GN_", GN)
                    qu = question.split()[0].lower()
                    if qu != "what":
                        question = question.replace("_action_", preds['what'])

                    result = self.qa_pipeline(question=question, context=clean_article_regex)
                    answer = result['answer']
                    score = result['score']

                    if score > scores[qu]:
                        preds[qu] = answer
                        scores[qu] = score
                    print(question, ' : ', answer, ' score : ', score)

                # display([ key + ": " + preds[key] + " (" + str(scores[key]) + ")"  for key in preds.keys()])
                print('\n')