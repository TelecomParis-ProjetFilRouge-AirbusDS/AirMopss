#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import fct
app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/new-article', methods=['POST'])
def new_article():
    session['article'] = request.form['article']
    session['word'] = session['article'].split()
    session['len'] = len(session['word'])
    session['list'] = fct(session['article'])
    session['event'] = 'text2'
    # blabla = qaprocessing.
    return render_template('article.html')

if __name__ == '__main__':
    app.run(debug=True)

