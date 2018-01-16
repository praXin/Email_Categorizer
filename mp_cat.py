import nltk
import random
import os
from nltk.tokenize import word_tokenize
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, NuSVC

def cat(text):
	p6 = open('my_logisticRegression_classifier.pickle','rb')
	LogisticRegression_classifier = pickle.load(p6)
	p6.close()
	print(LogisticRegression_classifier.classify(find_features(text)))
def find_features(document):
	features = {}
	p2 = open('my_word_features.pickle','rb')
	word_features = pickle.load(p2)
	p2.close()
	for w in word_features:
		features[w] = (w in words)
	return features