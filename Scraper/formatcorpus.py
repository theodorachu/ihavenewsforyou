import json
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import lda
import numpy as np
import random

ARTICLE_FILE = 'newsArticles.json'
STOP = set(stopwords.words('english'))
EXCLUDE = set(string.punctuation)
lemma = WordNetLemmatizer()
TRAIN_PERCENTAGE = .9
TEST_PERCENTAGE = .1

# json article object: { title, source, publishedDate, authors, url, summary, tags, text }
# input parameter: string of the name of the json file to be extracted
# output:
    # returns two corpora - one of just the titles in the json file and the other of the texts
        # these are in the format of an array where each index is an article's title or an article's text
# skips articles that don't have both titles and texts
# assumes that json is properly formatted
def extract_json(article_file):
    arr = []
    with open(article_file) as json_data:
        arr = json.load(json_data)
    corp_title = []
    corp_text = []
    used_articles = []
    for article in arr:
        if 'title' in article.keys() and 'text' in article.keys():
            corp_title.append(article['title'])
            corp_text.append(article['text'])
        else:
            continue
    return corp_title, corp_text

# function written with help of https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
# input parameter: string
# output: string minus all stop words and punctuation
def rm_stop_and_punc(article):
    without_stop = ' '.join([i for i in article.lower().split() if i not in STOP])
    without_punc = ''.join(ch for ch in without_stop if ch not in EXCLUDE)
    no_stop_no_punc = ' '.join(lemma.lemmatize(word) for word in without_punc.split())
    return no_stop_no_punc

# input parameter: corpus (aka array of articles)
# output:
    #id_to_word is a dictionary where the keys are the unique IDs of the words and the values are the words themselves
    # docterm is just a bag of words model of the input corpus 
        #(see https://en.wikipedia.org/wiki/Document-term_matrix for explanation of output)
        # to avoid sparse matrix, only maps (word_id, word_freq) tuples that exist in article instead of all ids plus frequencies
def create_docterm_matrix(corp):
    id_to_word = corpora.Dictionary(corp)
    docterm = [id_to_word.doc2bow(doc) for doc in corp]
    return id_to_word, docterm

# input parameters:
    # corpus = array of articles
    # id2word = dictionary of id mapped to word
    # passes = num of passes LDA algorithm makes on the data
    # num_topics = num of topics LDA algorithm splits data into
def train_lda(corpus, id2word, passes = 50, num_topics = 10):
    ldaModel = gensim.models.LdaModel
    lda = ldaModel(corpus, num_topics, id2word, False, passes)
    return lda

def apply_lda(model, docs, id2word):
    new_id2word = gensim.corpora.Dictionary()
    _ = new_id2word.merge_with(id2word)
    for doc in docs:
        print doc
        doc = new_id2word.doc2bow(doc)
        lda_topic = model[doc]
        a = list(sorted(lda_topic, key=lambda x: x[1]))
        print a[0]  # min probability topic
        print a[-1] # max probability topic
        print '\n'    

# input parameter: array corpus
# output: splits corpus into two corpora - a test and train one based on constant variables TRAIN_PERCENTAGE and TEST_PERCENTAGE
def get_test_and_train(corp):
    length = len(corp)
    num_train = int(length*TRAIN_PERCENTAGE)
    num_test = length - num_train
    train = np.sort(random.sample(xrange(length), num_train))
    train_corp = np.asarray(corp)[train]
    test = list(set(xrange(length))-set(train))
    test_corp = np.asarray(corp)[test]
    return train_corp, test_corp

def main():
    corp_title, corp_text = extract_json(ARTICLE_FILE)
    corp_title_clean = [rm_stop_and_punc(article).split() for article in corp_title]
    corp_text_clean = [rm_stop_and_punc(article).split() for article in corp_text]
    train_title, test_title = get_test_and_train(corp_title_clean)
    train_text, test_text = get_test_and_train(corp_text_clean)

    title_dict, corp_title_docterm = create_docterm_matrix(train_title)
    text_dict, corp_text_docterm = create_docterm_matrix(train_text)
    title_lda = train_lda(corp_title_docterm, title_dict)
    text_lda = train_lda(corp_text_docterm, text_dict)
    
    print title_lda.show_topics(-1, 5)
    apply_lda(title_lda, test_title, title_dict)
    apply_lda(text_lda, test_text, text_dict)

if __name__ == '__main__':
    main()
