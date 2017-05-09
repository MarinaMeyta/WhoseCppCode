from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re


def remove_short_words(words):
    return [i for i in words if len(i) >= 2]


def get_cppkeywords(filename):
    print('Getting cpp_keywords for', filename)
    remove_comments(filename)
    cpp_words = remove_short_words(
        re.split('[^a-z_]+', open('./tmp/output.cpp').read()))
    cpp_words = ' '.join(cpp_words)
    return cpp_words


def count_cppkeywords_tf(filenames):
    """Returns numpy array of keywords frequencies in each file"""

    keywords = re.split('[^a-z0-9_]+', open('./core/cpp_keywords.txt').read())
    vectorizer = TfidfVectorizer(vocabulary=keywords, use_idf=False)
    input_array = np.array([get_cppkeywords(filename) for filename in filenames])
    cpp_keywords_tf = vectorizer.fit_transform(input_array).toarray()
    return cpp_keywords_tf


def remove_comments(filename):
    """
    Removes comments from temporary file ./tmp/output.cpp
    in which the content of cpp-file was copied
    to prevent parsing commented lines
    and changing the original file
    """
    file = open(filename).read()
    result = re.split('//.*|/\*[\s\S]*?\*/|("(\\.|[^"])*")', file)
    tmp_file = open('./tmp/output.cpp', 'w+')  # encoding='cp1251', errors='ignore')
    result = filter(None, result)
    tmp_file.writelines(result)
    tmp_file.close()
