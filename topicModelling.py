# Let's read in our document-term matrix
import pandas as pd
import pickle

data = pd.read_pickle('dtm.pkl')

from gensim import matutils, models
import scipy.sparse

tdm = data.transpose()
tdm.head()

sparse_counts = scipy.sparse.csr_matrix(tdm)
corpus = matutils.Sparse2Corpus(sparse_counts)

cv = pickle.load(open("cv.pkl", "rb"))
id2word = dict((v, k) for k, v in cv.vocabulary_.items())

# print('\n2 topics\n')
# lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=2, passes=10)
# print(lda.print_topics())
#
# print('\n3 topics\n')
# lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=3, passes=10)
# print(lda.print_topics())
#
# print('\n4 topics\n')
# lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=4, passes=1000)
# print(lda.print_topics())

#Let's create a function to pull out nouns from a string of text
from nltk import word_tokenize, pos_tag


def nouns(text):
    '''Given a string of text, tokenize the text and pull out only the nouns.'''
    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = word_tokenize(text)
    all_nouns = [word for (word, pos) in pos_tag(tokenized) if is_noun(pos)]
    return ' '.join(all_nouns)

# Read in the cleaned data, before the CountVectorizer step
data_clean = pd.read_pickle('data_clean.pkl')
# print(data_clean)

# Apply the nouns function to the transcripts to filter only on nouns
data_nouns = pd.DataFrame(data_clean.fakenews.apply(nouns))
# print(data_nouns)

# Create a new document-term matrix using only nouns
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer

# Re-add the additional stop words since we are recreating the document-term matrix

stop_words = text.ENGLISH_STOP_WORDS

# Recreate a document-term matrix with only nouns
cvn = CountVectorizer(stop_words=stop_words)
data_cvn = cvn.fit_transform(data_nouns.fakenews)
data_dtmn = pd.DataFrame(data_cvn.toarray(), columns=cvn.get_feature_names())
data_dtmn.index = data_nouns.index
# print(data_dtmn)

# Create the gensim corpus
corpusn = matutils.Sparse2Corpus(scipy.sparse.csr_matrix(data_dtmn.transpose()))

# Create the vocabulary dictionary
id2wordn = dict((v, k) for k, v in cvn.vocabulary_.items())

# Let's start with 2 topics
# ldan = models.LdaModel(corpus=corpusn, num_topics=2, id2word=id2wordn, passes=10)
# print(ldan.print_topics())
# # Let's start with 3 topics
# ldan = models.LdaModel(corpus=corpusn, num_topics=3, id2word=id2wordn, passes=10)
# print(ldan.print_topics())
# # Let's start with 4 topics
# ldan = models.LdaModel(corpus=corpusn, num_topics=4, id2word=id2wordn, passes=10)
# print(ldan.print_topics())

# Let's create a function to pull out nouns from a string of text
def nouns_adj(text):
    '''Given a string of text, tokenize the text and pull out only the nouns and adjectives.'''
    is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'
    tokenized = word_tokenize(text)
    nouns_adj = [word for (word, pos) in pos_tag(tokenized) if is_noun_adj(pos)]
    return ' '.join(nouns_adj)

# Apply the nouns function to the transcripts to filter only on nouns
data_nouns_adj = pd.DataFrame(data_clean.fakenews.apply(nouns_adj))
# print(data_nouns_adj)

# Create a new document-term matrix using only nouns and adjectives, also remove common words with max_df
cvna = CountVectorizer(stop_words=stop_words, max_df=.8)
# print(cvna)
data_cvna = cvna.fit_transform(data_nouns_adj.fakenews)
# print(len(data_cvna.toarray()))
data_dtmna = pd.DataFrame(data_cvna.toarray(), columns=cvna.get_feature_names())
# print(data_dtmna)
data_dtmna.index = data_nouns_adj.index
# print(data_dtmna.index)


# Create the gensim corpus
corpusna = matutils.Sparse2Corpus(scipy.sparse.csr_matrix(data_dtmna.transpose()))

# Create the vocabulary dictionary
id2wordna = dict((v, k) for k, v in cvna.vocabulary_.items())

# # Let's start with 2 topics
# ldana = models.LdaModel(corpus=corpusna, num_topics=2, id2word=id2wordna, passes=10)
# print(ldana.print_topics())
# # Let's start with 2 topics
# ldana = models.LdaModel(corpus=corpusna, num_topics=3, id2word=id2wordna, passes=10)
# print(ldana.print_topics())
# # Let's start with 2 topics
# ldana = models.LdaModel(corpus=corpusna, num_topics=4, id2word=id2wordna, passes=10)
# print(ldana.print_topics())


# Our final LDA model (for now)
print("final LDA Model")
ldana = models.LdaModel(corpus=corpusna, num_topics=4, id2word=id2wordna, passes=10)
print(ldana.print_topics())



# Let's take a look at which topics each fakenews contains
corpus_transformed = ldana[corpusna]
topicFakenews=[]
index=0
for doc in corpus_transformed:
    preTopic= [index,doc]
    topicFakenews.append(preTopic)
    index=index+1
print(topicFakenews)


