#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spacy

from utils import *

def get_labels(pipeline: object = "ner", model: object = "en_core_web_sm") -> object:
    """
    Available names: ['tok2vec', 'tagger', 'parser', 'senter', 'ner', 'attribute_ruler', 'lemmatizer']
    """
    # L'ensemble des labels
    head(pipeline)
    nlp = spacy.load(model)
    for label in nlp.get_pipe(pipeline).labels:
        print(label, " -- ", spacy.explain(label))

def get_any_tag_label():
    print(spacy.glossary.GLOSSARY)

def explain(term):
    spacy.explain(term)

def get_infos(doc):
    deps = [word.dep_ for word in doc]  # extrait les dépendances entre les entités
    ents = list(doc.ents)  # doc.ents extrait les entités nommées
    print(ents[0].label)  # renvoie un nombre correspondant au label
    print(ents[0].label_)  # renvoie l'acronyme du label (ORG, PERSON,...)
    print(ents[0].text)  # renvoie le mot initial