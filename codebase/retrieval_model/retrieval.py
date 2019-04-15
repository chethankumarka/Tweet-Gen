# -*- coding: utf-8 -*-
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer

import numpy as np
import pickle
import random
import tensorflow as tf
import tflearn


stemmer = LancasterStemmer()
data = pickle.load( open("/home/sdhar3/Desktop/viraltweet/codebase/retrieval_model/training_data", "rb") )

words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

with open('/home/sdhar3/Desktop/viraltweet/codebase/retrieval_model/intent.json', "r") as json_data:
    intents = json.load(json_data)

tf.reset_default_graph()
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load('/home/sdhar3/Desktop/viraltweet/codebase/retrieval_model/model.tflearn')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

ERROR_THRESHOLD = 0.25

def classify(sentence):
    results = model.predict([bow(sentence, words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def response(sentence):
    results = classify(sentence)
    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    return random.choice(i['responses'])

            results.pop(0)

# while(True):
#     choice = raw_input("Please enter your choice: 1) Predict response for the tweet 2) Exit\n")
#     if int(choice)==1:
#         try:
#             tweet = str(raw_input("Enter the tweet\n"))
#             reply = response(tweet)
#             print(reply)
#         except Exception as e:
#             print("Unicode error! Please type again\n" + str(e))
#             continue
#     else:
#         break