import json
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora


class CorpusFormatter():
    def __init__(self):
        self.article_file = 'newsArticles.json'
        self.stop = set(stopwords.words('english'))
        self.exclude = set(string.punctuation)
        self.lemma = WordNetLemmatizer()


    # TODO: Currently just extracts the title and text
    # json article object: { title, source, publishedDate, authors, url, summary, tags, text }
    def extractContent(self, removeStopWords=True):
        articles = []
        with open(self.article_file) as json_data:
            articles = json.load(json_data)
       
        # Concatenates the title and text together (for now) 
        contents = []
        for article in articles:
            if 'title' in article.keys() and 'text' in article.keys():
                # Removes stop words if flag is set
                content = article['title'] + ' ' + article['text']
                contents.append(self.rm_stop_and_punc(content) if removeStopWords else content)
        return contents


    # function written with help of https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
    def rm_stop_and_punc(self, article):
        without_stop = ' '.join([i for i in article.lower().split() if i not in self.stop])
        without_punc = ''.join(ch for ch in without_stop if ch not in self.exclude)
        no_stop_no_punc = ' '.join(self.lemma.lemmatize(word) for word in without_punc.split())  
        return no_stop_no_punc


    def create_docterm_matrix(self, cleaned_corp):
        term_dict = corpora.Dictionary(cleaned_corp)
        return [term_dict.doc2bow(doc) for doc in cleaned_corp]

#def main():
#    corp_title, corp_text = extract_json(ARTICLE_FILE)
#    corp_title_clean = [rm_stop_and_punc(doc).split() for doc in corp_title]
#    corp_text_clean = [rm_stop_and_punc(doc).split() for doc in corp_text]
#    corp_title_docterm = create_docterm_matrix(corp_title_clean)
#    corp_text_docterm = create_docterm_matrix(corp_text_clean)

#if __name__ == '__main__':
#    main()
