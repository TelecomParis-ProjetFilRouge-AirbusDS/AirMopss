#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from .webapp_getpage import *
app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"



@app.route('/', methods=['GET'])
def index():
    app.logger.debug('index page loading')
    return render_template('index.html')

@app.route('/new-article', methods=['POST'])
def new_article():
    app.logger.warning('A new article processed (%d apples)', 42)
    session['article'] = request.form['article']
    session['word'] = session['article'].split()
    session['len'] = len(session['word'])
    session['list'] = fct(session['article'])
    session['event'] = 'text2'
    # blabla = qaprocessing.
    return render_template('article.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.error('An error occurred')
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


# if __name__ == '__main__':
#     app.run(debug=True)

