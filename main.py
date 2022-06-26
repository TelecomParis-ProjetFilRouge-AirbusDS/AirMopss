#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from airmopss import DataLoader
from airmopss import DataProcessing
from airmopss import utils
import logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)

def main(config):
    logging.info("Launching main process")

    # load data
    data_loader = DataLoader(config)

    # process
    data_processor = DataProcessing(config, data_loader)
    data_processor.run(task=config.task)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="How to launch airmopss")
    parser.add_argument('--csv_file', type=str, default='airmopss/data/newsdata.csv',
                        help="file of news wires (api format), default: data/newsdata.txt")
    parser.add_argument('--pkl_file', type=str, default="airmopss/data/newsdata_events.pkl")
    parser.add_argument('--labels_file', type=str, default='data/newsdata_labels.txt',
                        help="file of labeled articles, default: data/newsdata_labels.txt")
    parser.add_argument('--spacy_pipeline', type=str, default='en_core_web_sm',
                        help="chose spacy pipeline to use [en_core_web_sm], default: en_core_web_sm")
    parser.add_argument('--task', type=str, default='qa',
                        help="task to run [qa|summarize|extract_np|version], default: qa")
    parser.add_argument('--split', type=str, default='article',
                        help="splitting mode of content [article|paragraph], default: article")
    parser.add_argument('--labelled_only', type=utils.str2bool, default=True,
                        help="loads all data or labelled ones only, default: True")
    parser.add_argument('--debug_mini_load', type=utils.str2bool, default=False)
    config = parser.parse_args()

    main(config)

    # display different kind of labels
    # get_labels("ner")
    # get_labels("tagger")
    # get_labels("parser")
    #print(nlp.disabled)
    #create_ner_module("geopolitics_ner")


