import gensim
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np

stemmer = SnowballStemmer("english")
left_tweet_dataset = open('../../dataset/left_tweet_dataset.tsv', 'r')
data = left_tweet_dataset.readlines()
tweet_map = {}
for row in data:
	temp = row.split("\t")
	if temp[0] in tweet_map.keys():
		tweet_map[temp[0]] += 1
	else:
		tweet_map[temp[0]] = 1


stopwords = list(gensim.parsing.preprocessing.STOPWORDS)
stopwords.append("https")

def lemmatize_stemming(text):
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
	result=[]
	for token in gensim.utils.simple_preprocess(text) :
		if token not in stopwords and len(token) > 3:
			result.append(token)
	return result


processed_docs = []
for tweet in list(tweet_map.keys()):
	processed_docs.append(preprocess(tweet))


dictionary = gensim.corpora.Dictionary(processed_docs)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
lda_model =  gensim.models.LdaMulticore(bow_corpus, num_topics = 2, id2word = dictionary, passes = 50, workers = 2)

for index, topic in lda_model.print_topics(-1):
	print("Topic: {} \nWords: {}".format(index, topic))
	print("\n")