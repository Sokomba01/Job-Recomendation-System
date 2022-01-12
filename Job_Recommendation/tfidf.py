import pandas as pd
from sklearn.feature_extraction.text    import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# this is a very toy example, do not try this at home unless you want to understand the usage differences
docs = ["Talha Sarwar",
        "BSSE",
        "Web Development",
        "PHP, Django",
        "talhasarwar@gmail.com"
        ]
# instantiate CountVectorizer()
cv = CountVectorizer()

# this steps generates word counts for the words in your docs
word_count_vector = cv.fit_transform(docs)
print(word_count_vector.shape)
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)
# print idf values
df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(), columns=["idf_weights"])

# sort ascending
print(df_idf.sort_values(by=['idf_weights']))
# count matrix
count_vector = cv.transform(docs)

# tf-idf scores
tf_idf_vector = tfidf_transformer.transform(count_vector)
feature_names = cv.get_feature_names()

# get tfidf vector for first document
first_document_vector = tf_idf_vector[0]

# print the scores
df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
print(df.sort_values(by=["tfidf"], ascending=False))
from sklearn.feature_extraction.text import TfidfVectorizer

# settings that you use for count vectorizer will go here
tfidf_vectorizer = TfidfVectorizer(use_idf=True)

# just send in all your docs here
tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(docs)
# get the first vector out (for the first document)
first_vector_tfidfvectorizer = tfidf_vectorizer_vectors[0]

# place tf-idf values in a pandas data frame
df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names(),columns=["tfidf"])
df.sort_values(by=["tfidf"], ascending=False)
tfidf_vectorizer = TfidfVectorizer(use_idf=True)

# just send in all your docs here
fitted_vectorizer = tfidf_vectorizer.fit(docs)
tfidf_vectorizer_vectors = fitted_vectorizer.transform(docs)
