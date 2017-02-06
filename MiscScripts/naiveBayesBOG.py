# Trains a naive bayes classifier on corpuses from NLTK and tests on newsArticles.json, writing out the results to results/naiveBayesBOG.txt

# Tutorial followed: http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/

import json
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from corpusFormatter import CorpusFormatter

ARTICLE_FILE = 'newsArticles.json'

# FEATURE EXTRACTOR: bag of words
def word_feats(words):
    return dict([(word, True) for word in words])

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# Train the classifier
classifier = NaiveBayesClassifier.train(negfeats + posfeats)

# Obtain the title and text of news articles
formatter = CorpusFormatter()
testfeats = [word_feats(content.split(' ')) for content in formatter.extractContent()]

# 'Test' the classifier on newsArticles.json
predicted = classifier.classify_many(testfeats)

print predicted



