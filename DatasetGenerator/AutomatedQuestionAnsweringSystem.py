#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

"""Name:Query Interpretor
Author:Arihant Chhajed
Description:This module is for calculation of
semantic similarity using bag of word approach
between two sentenses using nltk tools."""

import string
import os
import sys
import logging
import re
import urllib.parse
from flask import Flask, jsonify, request
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from random import randint
import json

LEMMATIZER = WordNetLemmatizer()
APP = Flask(__name__)
CORS(APP)
logging.basicConfig()
CLASS_SET=["alumni","housing","counseling"]
KB={}
REMOVE_PUNCTUATION_MAP = dict((ord(char), None) for char in string.punctuation)
DICT = {}
CORPUS = {}
MODEL = {}
INDEX = {}
"""nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet') """

def model_generator(SetName):
    """
    it generate model and dictionary files for provided KB
    """
    try:
        global KB, DICT, MODEL, CORPUS, INDEX
        data = KB[x].keys()
        print(data)
        texts = [tokenize(doc) for doc in data if tokenize(doc) is not None]
        DICT[x]=corpora.Dictionary(texts)
        DICT[x].save("dataset/{}.dict".format(x))  # store the dictionary, for future reference
        CORPUS[x]=[DICT[x].doc2bow(text) for text in texts]
        # store to disk, for later use
        corpora.MmCorpus.serialize("dataset/{}.mm".format(x), CORPUS[x])
        MODEL[x]=models.LsiModel(CORPUS[x], id2word=DICT[x], num_topics=len(DICT[x]))
        INDEX[x]=similarities.MatrixSimilarity(
            MODEL[x][CORPUS[x]], num_features=len(DICT[x]))
        print("model generated succesfully")
        return "model generated succesfully"
    except Exception as ex:
        print(ex)
        return False


def get_wordnet_pos(treebank_tag):
    """
    Wordnet tree bank
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N') and treebank_tag.startswith('NN'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def pos_tagger(tokens):
    """
    postagger to find the parts of speech of the sentence
    """
    postagged = nltk.pos_tag(tokens)
    return postagged


def lematization(word, pos):
    """
    Lematization is the process to convert word into its most related morphological form.
    """
    tag = get_wordnet_pos(pos)
    if (tag is not ""):
        return LEMMATIZER.lemmatize(word, pos=tag)
    else:
        return LEMMATIZER.lemmatize(word)


def stop_word_filteration(tokens):
    """
    Filter commonly occured stop_words
    """
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in tokens if w not in stop_words]
    return filtered_sentence


def tokenize(sentence):
    """
    Tokenization
    """
    tokens = nltk.word_tokenize(
        sentence.lower().translate(REMOVE_PUNCTUATION_MAP))
    filtered_sentence = stop_word_filteration(tokens)
    pos_tagged = pos_tagger(filtered_sentence)
    lemma = []
    for (w, t) in pos_tagged:
        lemma.append(lematization(w, t))
    # for w in filtered_sentence:
    #     stemmed.append(stemming(w))
    return lemma


@APP.route('/question', methods=['POST'])
def run():
    """
    Run method to run QueryInterpreter for given query
    """
    print("Request recived by QueryInterpretor",request.json)
    response = {}

    try:
        obj = request.json
        input_query=obj['query']
        className=obj['class']
        print(input_query)
        if len(input_query.split()) >= 3:
            
            vec = DICT[className].doc2bow(tokenize(input_query))
            sims = INDEX[className][MODEL[className][vec]]
            ans = list(enumerate(sims))
            __max__ = 0
            max_index = -1
            for (index, per) in ans:
                if(per > __max__):                  
                    __max__ = per
                    max_index = index
            _threshold = 0.70
            if __max__ > _threshold and max_index is not -1:
                response['status'] = 200
                response['answer'] = KB[className][list(KB[className].keys())[max_index]]
            else:
                response['status'] = 201
                response['answer'] = "fallback"
            print("Confidence Score and index value is", __max__, max_index)
            return jsonify(response), 200
        else:
            response['status'] = 201
            response['answer'] = "fallback"
            return jsonify(response), 200
    except():
        response['status'] = 422
        error_msg = "An unexpected error as occured."
        response['message'] = error_msg + sys.exc_info()
        return jsonify(response)

def JSON_Loader(filename):
    with open(filename) as json_file:  
        data = json.load(json_file)
        return data


if __name__ == "__main__":
    try:
        print("Server started")
        for x in CLASS_SET:
            data = JSON_Loader("dataset/{}.json".format(x))
            KB[x]=data
            model_generator(x)
        APP.run(host='0.0.0.0', port=3000)
        print("app started at port 3000")
    except():
        print("An unexpected error occured")
