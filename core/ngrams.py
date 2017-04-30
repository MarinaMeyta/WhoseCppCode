from sklearn.feature_extraction.text import CountVectorizer
from core.whose_cpp_code import get_filenames

filenames, authors = get_filenames('/media/marina/hdd/diploma/data/c++/data/')

vectorizer = CountVectorizer(input='filename', analyzer='char_wb', ngram_range=(1, 3), min_df=0)
dtm = vectorizer.fit_transform(filenames).toarray()
vocab = vectorizer.get_feature_names()  # a list

print(dtm)
print(vocab)
