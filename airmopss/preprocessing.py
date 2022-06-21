#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The module declares preprocessing utility functions
"""

import re


def get_stop_sentences():
    """
    Returns a list of sentences that should be excluded from source

    :return: list of str
    """
    stops = [stp for lst in _stop_sentences for stp in lst]
    return stops


stop_sentences_reuters = [
    "Register now for FREE unlimited access to Reuters.com Register",
    "Our Standards: The Thomson Reuters Trust Principles.",
]

stop_sentences_any = [
    "Advertisement",
    "Get in touch",
    "Go to https://apnews.com/hub/russia-ukraine for more coverage",
    "Share on Twitter",
    "Share via Email",
    "Share on Facebook"
]

_stop_sentence_patterns = [
    "Other {{#cta}} {{text}} {{/cta}} Email address Please enter a valid email address Please enter your email address Set a reminder Sorry we couldn't set a reminder for you this time. Please try again later. . To find out what personal data we collect and how we use it, view our We will send you a maximum of two emails in. To find out what personal data we collect and how we use it, view our Privacy Policy . If you have any questions about contributing, please We will be in touch to remind you to contribute. Look out for a message in your inbox in. If you have any questions about contributing, please contact us {{/paragraphs}}{{#choiceCards}}{{/choiceCards}}",
    "{{#choiceCards}}",
    "{{topLeft}} {{bottomLeft}} {{topRight}} {{bottomRight}} {{/goalExceededMarkerPercentage}} {{#goalExceededMarkerPercentage}}{{/goalExceededMarkerPercentage}} {{heading}} {{#paragraphs}} {{#ticker}}{{/ticker}}{{#paragraphs}} {{.}} {{/paragraphs}} {{highlightedText}}",
    "Reporting by john Chalmers, Gabriela Baczynska",
    "Reporting by Reuters; editing by Guy Faulconbridge",
    "Reporting by Leah Douglas; Editing by Alison Williams and David Gregorio",
    "Reporting by Stanley Widianto and Angie Teo Writing by Ed Davies Editing by Kanupriya Kapoor",
    "Reporting by Nidhi Verma; Editing by Aditya Soni",
    "Reporting by Phuong Nguyen Editing by Ed Davies",
    "Reporting by Jarrett Renshaw on aboard Afir Force One and Trevor Hunnicutt in Washington; Additional reporting by Alexandra Alper; Editing by Heather Timmons, Mary Milliken and Cynthia Osterman",
    "Show caption......",
]

_stop_sentences = [
    stop_sentences_reuters,
    stop_sentences_any
]

_unwanted_sequences = [
    "Show caption",
    "Getty images",
    # "@"
]

stop_sentences = get_stop_sentences()


def article_to_list(txt):
    """
    Returns the text as a list. Split on end of line.

    :param txt:
    :return:
    """

    return txt.split('\n')


def remove_stop_sentences(l_txt):
    """
    Removes complete sentences from a list.

    :param l_txt: full list
    :return: processed list
    """

    l_txt = [stp for stp in l_txt if stp not in stop_sentences]
    return l_txt


def remove_unwanted_sequences(l_txt):
    """
    Removes parts of sentences from a list of sentences.

    :param l_txt:
    :return: processed list
    """
    for pattern in _unwanted_sequences:
        l_txt = [valid_seq for valid_seq in l_txt if pattern not in valid_seq]
    return l_txt


def remove_short_lines(l_txt, min_num_words=10):
    """
    Removes sentences that are composed of less than 'min_num_words' words.

    :param l_txt:
    :param min_num_words: defaults to 10
    :return: processed list
    """
    l_txt = [line for line in l_txt if len(line.split(' ')) > min_num_words]
    return l_txt


def list_to_text(lst):
    r"""
    Concatenates elements a list in a string separated by character eol '\n'

    :param lst:
    :return:
    """
    return "\n".join(lst)


def clean_text(txt, min_num_words=10):
    """
    Pipeline of preprocessing over the text 'txt':
    * removal of unwanted sentences (stop sentences),
    * removal of sentences containing unwanted patterns,
    * removal of sentences a minimal length.

    :param txt: a string (str) of text
    :param min_num_words:
    :return: a list of sentences
    """

    l_txt = article_to_list(txt)
    l_txt = remove_stop_sentences(l_txt)
    l_txt = remove_unwanted_sequences(l_txt)
    l_txt = remove_short_lines(l_txt, min_num_words)
    return list_to_text(l_txt)


def tokens_to_list_unique(tokens):
    """
    TODO to complete

    :param tokens:
    :return:
    """
    lst = [" ".join([str(elt) for elt in token]).strip() for token in tokens]
    lst = list(dict.fromkeys(lst))
    return lst


def split_paragraphs(txt):
    """
    Splits the text 'txt' into paragraphs.

    The splitting pattern is two consecutive EOL or two EOL separated by space characters.

    :param txt: a string (str) of text
    :return: a list of sentences
    """
    _cleaned = re.sub("\n\S+\n\n+", "\n", txt)
    _cleaned = re.sub("\n+", "\n", _cleaned)
    paragraphs = _cleaned.split('\n')
    ## useless ? 
    # paragraphs = [paragraph for paragraph in paragraphs]
    return paragraphs


if __name__ == '__main__':
    s = "test\n\ntsdqfd gshsh st hsrh rshvc rshs r h f e s  t\n\nGetty images c b n j k lm u y fdsqdfqsdq\n\nHacked Gitty imiges c b n j k lm u y fdsqdfqsdq\n" + "Share on Twitter\n"

    print("\n### s : \n", s)
    print("\n### clean : \n", clean_text(s))
    print("\n### paragraphs: \n", split_paragraphs(clean_text(s)))
