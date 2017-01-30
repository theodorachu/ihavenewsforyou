import json
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

# function written with help of https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
def rm_stop_and_punc(article):
    without_stop = ' '.join([i for i in article.lower().split() if i not in stop])
    without_punc = ''.join(ch for ch in without_stop if ch not in exclude)
    no_stop_no_punc = ' '.join(lemma.lemmatize(word) for word in without_punc.split())
    return no_stop_no_punc

### json article object:
### { title, source, publishedDate, authors, url, summary, tags, text }

arr = json.load('newsArticles.json')
corp_title = []
corp_text = []
for article, idx in enumerate(arr):
    corp_title.add(article['title'])
    corp_text.add(article['text'])

corp_title_clean = [rm_stop_and_punc(doc).split() for doc in corp_title]
corp_text_clean = [rm_stop_and_punc(doc).split() for doc in corp_text_clean]


