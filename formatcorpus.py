import json
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora

ARTICLE_FILE = 'newsArticles.json'
STOP = set(stopwords.words('english'))
EXCLUDE = set(string.punctuation)
lemma = WordNetLemmatizer()

# json article object: { title, source, publishedDate, authors, url, summary, tags, text }
def extract_json(article_file):
    arr = json.load(article_file)
    corp_title = []
    corp_text = []
    for article, idx in enumerate(arr):
        corp_title.add(article['title'])
        corp_text.add(article['text'])
    return corp_title, corp_text

# function written with help of https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
def rm_stop_and_punc(article):
    without_stop = ' '.join([i for i in article.lower().split() if i not in STOP])
    without_punc = ''.join(ch for ch in without_stop if ch not in EXCLUDE)
    no_stop_no_punc = ' '.join(lemma.lemmatize(word) for word in without_punc.split())
    return no_stop_no_punc

def create_docterm_matrix(cleaned_corp):
    term_dict = corpora.Dictionary(cleaned_corp)
    return [dictionary.doc2bow(doc) for doc in cleaned_corp)

def main():
    corp_title, corp_text = extract_json(ARTICLE_FILE)
    corp_title_clean = [rm_stop_and_punc(doc).split() for doc in corp_title]
    corp_text_clean = [rm_stop_and_punc(doc).split() for doc in corp_text_clean]
    corp_title_docterm = create_docterm_matrix(corp_title_clean)
    corp_text_docterm = create_docterm_matrix(corp_text_clean)

if __name__ == '__main__':
    main()
