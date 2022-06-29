#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import argparse
import json

from ..dataloader import DataLoader
from ..dataprocessing import DataProcessing
from ..qaprocessing import QaProcessing
import logging

logging.info(f"Building Flask app...")
app = Flask(__name__)

app.secret_key = "SekretKi"

# TODO : to fix as it, duplicates argarse from main.py
config = argparse.Namespace()
config.csv_file='airmopss/data/newsdata.csv'
config.pkl_file='airmopss/data/newsdata_events.pkl'
config.labels_file='airmopss/data/newsdata_labels.txt'
config.spacy_pipeline='en_core_web_sm'
config.task='qa'
config.split='article'
config.labelled_only=True

data_loader = DataLoader(config, logger=app.logger)
data_processor = DataProcessing(config, data_loader, logger=app.logger)
qa_processor = QaProcessing(config, data_loader, logger=app.logger)

article_events = data_loader.load_data_articles_pkl(config.pkl_file)

@app.route('/', methods=['GET'])
def index():
    """
    Renders the main page. Displays a dropdown list of dataset articles and a textarea to process any text.

    :return:
    """
    app.logger.debug('index page loading')

    article_ids = list(article_events.keys())
    article_titles = [data_loader.get_data_title(article_id) for article_id in article_ids]

    return render_template('index.html', 
        article_nb=len(article_ids),
        article_ids=article_ids, 
        article_titles=article_titles,
    )

@app.route('/events', methods=['POST'])
def events():
    """
    Renders the page which displays extracted events and the validation buttons.

    :return:
    """
    if request.form['data_origin'] == 'dataset':
        # TODO: Fix issue with indices shift
        article_id = int(request.form['article_id'])
        article = data_loader.get_data_content_full(article_id)
        events = article_events[article_id]
        events_list = [(event["start_idx"], event["end_idx"], json.dumps(event["details"])) for event in events["events"]]

        return render_template('event.html', article=article, article_len=len(article), events=events, events_list=events_list)

    else:
        article = request.form['article']
        # TODO handle the case where events is None
        events = qa_processor.get_events(article)
        events_list = [(event["start_idx"], event["end_idx"], json.dumps(event["details"])) for event in events["events"]]

        return render_template('event.html', article=article, article_len=len(article), events=events, events_list=events_list)
