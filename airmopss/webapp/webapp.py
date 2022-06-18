#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from .webapp_getpage import *
import argparse

from ..dataloader import DataLoader
from ..dataprocessing import DataProcessing
from ..qaprocessing import QaProcessing
import logging

logging.info(f"Building Flass app...")
app = Flask(__name__)

app.secret_key = "SekretKi"

# ugly
# TODO : to fix as it, duplicates argarse from main.py
config = argparse.Namespace()
config.csv_file='airmopss/data/newsdata.csv'
config.labels_file='airmopss/data/newsdata_labels.txt'
config.spacy_pipeline='en_core_web_sm'
config.task='qa'
config.split='article'
config.labelled_only=True

data_loader = DataLoader(config)
data_processor = DataProcessing(config, data_loader)
qa_processor = QaProcessing(config, data_loader)

@app.route('/', methods=['GET'])
def index():
    app.logger.debug('index page loading')
    return render_template('index.html')

@app.route('/new-article', methods=['POST'])
def new_article():
    article = request.form['article']

    # TODO: article includes \r after \n. Should they be removed ?
    app.logger.warning(repr(article))

    events = qa_processor.get_events(article)
    indices_list = [(event["start_idx"], event["end_idx"]) for event in events["events"]]

    return render_template('article.html', article=article, article_len=len(article), events=events, indices_list=indices_list)

# if __name__ == '__main__':
#     app.run(debug=True)

