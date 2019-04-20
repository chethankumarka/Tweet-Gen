# -*- coding: utf-8 -*-
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer

import numpy as np
import pickle
import random
import tensorflow as tf
import tflearn

import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string
from collections import Counter
import operator
import math

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


######
#Accuracy for left tag: 14/19
#Accuracy for right tag: 152/159 
######

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

tokenizer = nltk.tokenize.TreebankWordTokenizer()

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

tags = []
output_analysis = open("right_analysis.csv", "w")
def response(sentence):
    global tags
    global output_analysis

    results = classify(sentence)
    print(results)

    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    tags.append(i['tag'])
                    res = fetch_response(sentence, i['patterns'], i['responses'])
                    output_analysis.write("right," + str(results[0][0]) + "," + str(results[0][1]) + "," + res[0].strip() + "," + res[1].strip() + "\n")
                    # return random.choice(i['responses'])

            results.pop(0)

def fetch_response(input_tweet, tweets, responses):
    js_map = {}
    cs_map = {}

    tokens_input = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(input_tweet) \
    if token.lower().strip(string.punctuation) not in stopwords]

    for index, tweet in enumerate(tweets):
        tokens_tweet = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(tweet) \
        if token.lower().strip(string.punctuation) not in stopwords]

        js_map[index] = jaccard_similarity(tokens_input, tokens_tweet)
        cs_map[index] = similarity(tokens_input, tokens_tweet)

    sorted_js = sorted(js_map.items(), key=operator.itemgetter(1), reverse=True)
    sorted_cs = sorted(cs_map.items(), key=operator.itemgetter(1), reverse=True)
    
    # print("##### Jaccard similar response:" + responses[sorted_js[0][0]])
    # print("##### Cosine similar response:" + responses[sorted_cs[0][0]])
    return [responses[sorted_js[0][0]], responses[sorted_cs[0][0]]]

def jaccard_similarity(tokens_input, tokens_tweet):
    return len(set(tokens_input).intersection(tokens_tweet)) / float(len(set(tokens_input).union(tokens_tweet)))

def similarity(tokens_input, tokens_tweet):
    counter_input, counter_tweet = Counter(tokens_input), Counter(tokens_tweet)
    return length_similarity(counter_input, counter_tweet) * cosine_similarity(counter_input, counter_tweet)

def cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def length_similarity(c1, c2):
    lenc1 = sum(c1.itervalues())
    lenc2 = sum(c2.itervalues())
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))

def accuracy():
    global tags

    print("Accuracy:" + str(tags.count("right")*100/len(tags)))

def ui_response(sentence):
    results = classify(sentence)

    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    res = fetch_response(sentence, i['patterns'], i['responses'])
                    return [i['tag'], res[0], res[1]]

# f = open("test_right_tweet_dataset.tsv", "r")
# data = f.readlines()
# for row in data:
#     response(row.strip().split("\t")[0].encode('utf-8'))
#     print("\n")
# accuracy()

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