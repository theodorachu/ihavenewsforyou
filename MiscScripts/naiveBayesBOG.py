# Trains a naive bayes classifier on corpuses from NLTK and tests on newsArticles.json, writing out the results to results/naiveBayesBOG.txt

# Tutorial followed: http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from corpusFormatter import CorpusFormatter

ARTICLE_FILE = 'newsArticles.json'
OUTPUT_FILE = 'results/naiveBayesBOG.txt'

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
contents = formatter.extractContent()
testfeats = [word_feats(content.split(' ')) for content in contents]

# 'Test' the classifier on newsArticles.json
predicted = classifier.classify_many(testfeats)

# Write the predicted for observation
negArticles = []
posArticles = []
for i, label in enumerate(predicted):
    if label == 'neg':
       negArticles.append(''.join(contents[i][:100])) 
    else:
       posArticles.append(''.join(contents[i][:100]))

output = open(OUTPUT_FILE, 'w')
output.write('NEGATIVE -----------------------------\n')
for article in negArticles:
    output.write(article.encode('utf8') + '\n')
output.write('POSITIVE -----------------------------\n')
for article in posArticles:
    output.write(article.encode('utf8') + '\n')
output.close()
