import random
import numpy as np
from corpusInterface import CorpusInterface
from nltk.classify import NaiveBayesClassifier
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression

ARTICLE_FILE = 'newsArticles.json'

corpusInterface = CorpusInterface()
contents = corpusInterface.extractContent()

left = []
right = []
center = []
for content in contents:
  label = content['bias'][6:]
  if label == 'Left' or label == 'Lean Left':
    left.append(content)
  elif label == 'Right' or label == 'Lean Right': 
    right.append(content)
  elif label == 'Center' or label == 'Mixed':
    center.append(content)

random.shuffle(left)
random.shuffle(right)
random.shuffle(center)

# FEATURE EXTRACTOR: bag of words
def word_feats(words):
  return dict([(word, True) for word in words])

# NAIVE BAYES
left = [(word_feats(corpusInterface.rm_stop_and_punc(x['title'] + " " + x['text']).split(' ')), 'left') for x in left]
right = [(word_feats(corpusInterface.rm_stop_and_punc(x['title'] + " " + x['text']).split(' ')), 'right') for x in right]
center = [(word_feats(corpusInterface.rm_stop_and_punc(x['title'] + " " + x['text']).split(' ')), 'center') for x in center]

# TRAIN 
trainfeats = left[:-20] + right[:-20] + center[:-20]
#classifier = NaiveBayesClassifier.train(trainfeats) # NAIVE BAYES
classifier = SklearnClassifier(LogisticRegression()).train(trainfeats)

# TEST
testfeats = [x[0] for x in (left[-20:] + right[-20:] + center[-20:])]
total = len(testfeats)
numLeftWrong = 0
numRightWrong = 0
numCenterWrong = 0
for i in xrange(len(testfeats)):
  predicted = classifier.classify(testfeats[i])
  if i < 20 and predicted != 'left':
    numLeftWrong += 1
  elif i >= 20 and i < 40 and predicted != 'right':
    numRightWrong += 1
  elif i >= 40 and predicted != 'center':
    numCenterWrong += 1

totalWrong = numLeftWrong + numRightWrong + numCenterWrong
print "Accuracy: (" + str(total - totalWrong) + "/" + str(total) + ") = " + str(float(total - totalWrong) / total) + '%'
print "Left Accuracy: (" + str(20 - numLeftWrong) + "/" + str(20) + ")"
print "Right Accuracy: (" + str(20 - numRightWrong) + "/" + str(20) + ")"
print "Center Accuracy: (" + str(20 - numCenterWrong) + "/" + str(20) + ")"