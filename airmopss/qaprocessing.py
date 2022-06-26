#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The module handles the Question Answering processing class
"""

from .preprocessing import *
from .dataloader import DataLoader

from transformers import pipeline
import logging

class QaProcessing():
    """
    The class QaProcessing handles the QA task.
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

        self.data_loader = data_loader

        # TODO : to remove before delivery
        if config.debug_mini_load:
            pass
        else:
            self.spacy_pipeline = data_loader.pipeline
            self.qa_pipeline = pipeline("question-answering")  # , model="distilbert-base-cased-distilled-squad", tokenizer="bert-base-cased")

        self.questions = self.set_questions()

    def set_questions(self):
        """
        List of patterns of questions

        :return:
        """
        questions = [
            "What happened to _GN_?",
            "What happens to _GN_?",
            "What did _GN_ do?",
            "What do _GN_ do?",

            "When did _GN_ _action_?",
            "When do _GN_ _action_?",
            "When did _action_ happen?",

            "Where did _GN_ _action_?",
            "Where do _GN_ _action_?",
            "Where did _action_ take place?"
        ]
        return questions

    def ask_question(self):
        """
        Handles command line input question
        """
        while True:
            q = input("Enter a question: ")
            if q == "#": break
            print(q)


    def get_gn_subjs(self, doc, increment=0):
        """
        Extraire l'ensemble des groupes nominaux sujets (non-pronominaux) qui sont des entités ['GPE', 'PERSON', 'ORG', 'NORP'] et les index de début et de fin

        Renvoie deux listes : [GN1, GN2, GN3, ...] et leurs index dans doc [[start_gn1, stop_gn1],[start_gn2 , stop_gn2],[start_gn3 , stop_gn3], ...]

        :param doc:
        :return (list,list):
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
                    idx = [word_index[0] + increment, word_index[-1] + word_len[-1] + increment]
                    gn_subj_idx.append(idx)

        # reconcatene en liste de string
        gn_subj = [" ".join([str(elt) for elt in GN]).strip() for GN in np_list_subj]
        gn_subj = list(dict.fromkeys(gn_subj))

        return gn_subj, gn_subj_idx

    # TODO : complete function (DONE)
    def get_events(self, input_txt):
        """
        Fonction qui à partir d'un input_txt, le preprocess et extrait les évènements pour renvoyer un json destiné à l'affichage webapp

        [{ "start_idx": int, 
            "end_idx" : int,
            "details" : {
                "Who" : str,
                "What" : str,
                "When" : str,
                "Where" : str
            }}, ... ]

        :param input_txt:
        :return list:
        """

        # preprocessing step
        text_clean = clean_text(input_txt)

        # split in paragraphs
        paragraphs = split_paragraphs(text_clean)

        return self.extract_events(input_txt, text_clean, paragraphs)

    def get_events_by_article(self, id_article):

        article = self.data_loader.get_data_content_full(id_article)
        text_clean = self.data_loader.get_data_content_clean(id_article)
        # TODO  : chekc split in paragraph consistency
        paragraphs = self.data_loader.get_data_content_paragraphs(id_article)

        return self.extract_events(article, text_clean, paragraphs)

    def extract_events(self, input_txt, text_clean, paragraphs):
        # mapping between the indices of the raw article and the cleaned article
        mapping_dict = self.data_loader.get_aligned_indices(input_txt, text_clean)
        #mapping_dict = self.data_loader.get_aligned_indices(input_txt, "\n".join(paragraphs))

        
        gn_subj_all = []
        gn_subj_idx_all = []
        answers_all = []
        paragraph_len = 0
        
        for paragraph in paragraphs:
            
            doc = self.spacy_pipeline(paragraph)
            gn_subj, gn_subj_idx = self.get_gn_subjs(doc, increment = paragraph_len)
        
            gn_subj_idx_all += gn_subj_idx
            gn_subj_all += gn_subj

            for GN in gn_subj:

                scores = {'what': 5e-3, 'who': 5e-3, 'when': 5e-2, 'where': 5e-2}
                # preds = {'what':None, 'who':None, 'when':None, 'where':None}
                preds = {'what': "XXX", 'who': GN, 'when': "XXX", 'where': "XXX"}
                id_start = {'what': 0, 'who': gn_subj_idx[0][0], 'when': 0, 'where': 0}
                id_end = {'what': 0, 'who': gn_subj_idx[0][1], 'when': 0, 'where': 0}

                answers_gn = []

                for idx, question in enumerate(self.questions):

                    question = question.replace("_GN_", GN)
                    qu = question.split()[0].lower()
                    if qu != "what":
                        question = question.replace("_action_", preds['what'])

                    result = self.qa_pipeline(question=question, context=paragraph)
                    score = result['score']

                    #self.logger.info(f"Result is {result}\nAnswer to question {question} : \n {answer}\nScore: {score}\n------------------------------------------")
                    #answers_gn.append([answer, id_start, id_end, score])

                    if score > scores[qu]:
                        preds[qu] = result['answer']
                        scores[qu] = score
                        id_start[qu] = result['start'] + paragraph_len
                        id_end[qu] = result['end'] + paragraph_len

                answers_gn = [[preds[qu], id_start[qu], id_end[qu], scores[qu] ] for qu in ['what', 'when','where']]
                answers_all.append(answers_gn)
                
                self.logger.info(answers_gn)
                #self.logger.info(answers_all)

            ## Update the character count variable
            paragraph_len += len(paragraph)+1
        

        events = { "events" :
                       [{ "start_idx": mapping_dict[gn_subj_idx_all[i][0]],
                        "end_idx" : mapping_dict[gn_subj_idx_all[i][1]],
                        "details" : {
                            # "Who" : [ gn_subj_all[i], idx_start, id_end],
                            "Who" : gn_subj_all[i],
                            "What" : {
                                "answer": answers_all[i][0][0],
                                "id_start": mapping_dict[answers_all[i][0][1]],
                                "id_end": mapping_dict[answers_all[i][0][2]],
                                "score": answers_all[i][0][3],
                            },
                            # answers_all[i][0]
                            "When" : {
                                "answer": answers_all[i][1][0],
                                "id_start": mapping_dict[answers_all[i][1][1]],
                                "id_end": mapping_dict[answers_all[i][1][2]],
                                "score": answers_all[i][1][3],
                            },
                            #answers_all[i][1],
                            "Where" : {
                                "answer": answers_all[i][2][0],
                                "id_start": mapping_dict[answers_all[i][2][1]],
                                "id_end": mapping_dict[answers_all[i][2][2]],
                                "score": answers_all[i][2][3],
                            },
                            #answers_all[i][2]
                            }
                    } for i in range(len(gn_subj_all)) ]}

        return events

    def process_and_store(self):
        newsdata_events = {}
        #for id_article in self.data_loader.data.keys():
        for id_article in [0, 1, 101]:

            self.logger.info(id_article)
            # for id_article in [1]:
            article = self.data_loader.get_data_content_full(id_article)

            text_clean = self.data_loader.get_data_content_clean(id_article)
            # TODO  : check split in paragraph consistency
            paragraphs = self.data_loader.get_data_content_paragraphs(id_article)

            events = self.extract_events(article, text_clean, paragraphs)
            newsdata_events[id_article] = events

        self.data_loader.save_data_articles_pkl(newsdata_events, filename="newsdata_events.pkl")


    def process(self):
        """

        :return:
        """
        #articles = self.data[2]
        # TODO : to extend or fix depending on desired process
        for idx in [101]:

            #clean_article_regex = re.sub("\n\S+\n\n+", "\n", articles[idx])
            #clean_article_regex = re.sub("\n+", "\n", clean_article_regex)
            
            ## If launched from terminal 
            article = self.data_loader.get_data_content_full(idx)
            paragraphs = self.data_loader.get_data_content_paragraphs(idx)

            gn_subj_all = []
            gn_subj_idx_all = []
            answers_all = []
            paragraph_len = 0

            for paragraph in paragraphs:
                
                print(paragraph, end='\n\n')

                doc = self.spacy_pipeline(paragraph)
                gn_subj, gn_subj_idx = self.get_gn_subjs(doc, increment = paragraph_len)
            
                gn_subj_idx_all += gn_subj_idx
                gn_subj_all += gn_subj

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
                        #else:
                        #    print("Score too low")

                        #print(question, ' : ', answer, ' score : ', score)

                    answers_all += answers_gn

                    # display([ key + ": " + preds[key] + " (" + str(scores[key]) + ")"  for key in preds.keys()])
                    #print('\n')

                ## Update the character count variable
                paragraph_len += len(paragraph)

        print(answers_all)

        return answers_all