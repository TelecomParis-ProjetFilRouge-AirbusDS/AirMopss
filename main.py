#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from airmopss import DataLoader
from airmopss import DataProcessing
from airmopss import utils
import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

def main(config):
    logging.info("Launching main process")
    # load data
    data_loader = DataLoader(config)

    # process
    data_processor = DataProcessing(config, data_loader)
    data_processor.run(task="qa")

    #create_ner_module("geopolitics_ner")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="How to launch airmopps")
    parser.add_argument('--csv_file', type=str, default='data/newsdata.csv', help="file of news wires (api format), default: data/newsdata.txt")
    parser.add_argument('--labels_file', type=str, default='data/newsdata_labels.txt', help="file of labeled articles, default: data/newsdata_labels.txt")
    parser.add_argument('--pipeline', type=str, default='en_core_web_sm', help="chose spacy pipeline to use [en_core_web_sm], default: en_core_web_sm")
    parser.add_argument('--task', type=str, default='qa', help="task to run [qa|summarize|extract_np|version], default: qa")
    parser.add_argument('--split', type=str, default='article', help="spliting mode of content [article|paragraph], default: article")
    parser.add_argument('--labelled_only', type=utils.str2bool, default=True, help="loads all data or labelled ones only, default: True")
    config = parser.parse_args()

    main(config)

    # parser.add_argument("--decay_epoch", type=int, default=100, help="epoch from which to start lr decay")
    # parser.add_argument("--n_cpu", type=int, default=8, help="number of cpu threads to use during batch generation")
    # parser.add_argument("--lambda_cyc", type=float, default=10.0, help="cycle loss weight")
    # parser.add_argument('--cuda_parallel', type=str2bool, default=False)
    # parser.add_argument('--epochs', type=int, default=40000, help="number of epochs of training")
    # parser.add_argument('--datasets_path', type=str, default='~/datasets')


    # display diffent kind of labels
    # get_labels("ner")
    # get_labels("tagger")
    # get_labels("parser")
    #print(nlp.disabled)


