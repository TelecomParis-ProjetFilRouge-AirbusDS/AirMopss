#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from .webapp_getpage import *
import argparse
import json

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
config.pkl_file='airmopss/data/newsdata_events.pkl'
config.labels_file='airmopss/data/newsdata_labels.txt'
config.spacy_pipeline='en_core_web_sm'
config.task='qa'
config.split='article'
config.labelled_only=True

# TODO : to remove before delivery
config.debug_mini_load = False

data_loader = DataLoader(config, logger=app.logger)
data_processor = DataProcessing(config, data_loader, logger=app.logger)
qa_processor = QaProcessing(config, data_loader, logger=app.logger)

@app.route('/', methods=['GET'])
def index():
    app.logger.debug('index page loading')
    return render_template('index.html')

@app.route('/events', methods=['POST'])
def events():
    article = request.form['article']

    # TODO: article includes \r after \n. Should they be removed ?
    #app.logger.warning(repr(article))

    events = qa_processor.get_events(article)

    events_list = [(event["start_idx"], event["end_idx"], json.dumps(event["details"])) for event in events["events"]]
    #app.logger.info(events_list)

    return render_template('event.html', article=article, article_len=len(article), events=events, events_list=events_list)

# if __name__ == '__main__':
#     app.run(debug=True)

