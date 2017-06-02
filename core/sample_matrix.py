import re
import math
import time
import numpy as np
import os.path
import warnings
from core.whose_cpp_code import get_filenames
from core.lexical_features import get_lexical_features
from core.cpp_keywords import count_cppkeywords_tf


warnings.filterwarnings("ignore")


def save_matrix(outfile, outpath, matrix):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    file_path_name = os.path.join(outpath, outfile)
    if os.path.exists(file_path_name):
        np.save(file_path_name, matrix)
    else:
        open(file_path_name, 'w+', encoding='utf-8').close()
        np.save(file_path_name, matrix)


def get_sample_matrix(path, outpath):
    start_time = time.time()
    filenames, authors = get_filenames(path)
    save_matrix('authors.npy', outpath, authors)
    save_matrix('filenames.npy', outpath, filenames)

    lexical_features = [get_lexical_features(filename) for filename in filenames]
    save_matrix('lexical_features.npy', outpath, lexical_features)

    cpp_keywords_tf = count_cppkeywords_tf(filenames)
    save_matrix('cpp_keywords_tf.npy', outpath, cpp_keywords_tf)

    # lexical_features = np.load(os.path.join(outpath, 'lexical_features.npy'))
    # cpp_keywords_tf = np.load(os.path.join(outpath, 'cpp_keywords_tf.npy'))
    matrix = np.hstack((lexical_features, cpp_keywords_tf))
    save_matrix('matrix.npy', outpath, matrix)

    # print(len(np.load(os.path.join(outpath, 'matrix.npy'))))
    run_time = time.time() - start_time
    # print('Run time: ', run_time)
