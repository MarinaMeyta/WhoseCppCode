import os.path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from collections import OrderedDict
# import matplotlib.pyplot as plt
from core.lexical_features import get_lexical_features
from core.syntactic_features import get_syntactic_features
from core.cpp_keywords import count_cppkeywords_tf
from sklearn.model_selection import train_test_split
import time
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
import re
from itertools import compress
from sklearn.model_selection import cross_val_score, KFold

from sklearn.ensemble import GradientBoostingClassifier
import json


def get_filenames(path_to_data):
    filenames_list = np.array([])
    authors = np.array([])
    for dirpath, dirnames, filenames in os.walk(path_to_data):
        for filename in [f for f in filenames if f.endswith(".cpp")]:
            authors = np.append(authors, os.path.basename(dirpath))
            filenames_list = np.append(filenames_list, os.path.join(dirpath, filename))
    return filenames_list, authors


def get_sample_matrix(filenames):
    # features = np.array([lexical_features.get_lexical_features(filename) +
    # syntactic_features.get_syntactic_features(filename) for filename in
    # filenames])
    features = np.array([get_lexical_features(filename) for filename in filenames])
    keywords = count_cppkeywords_tf(filenames)
    matrix = np.hstack((features, keywords))
    return matrix


# import csv
#
# # TODO: save to csv, not txt


# def write_report(report, num_of_features, y_true, y_pred, probabilities, accuracy, run_time, feature_importances):
#
#     lines = report.split('\n')
#     row_data = lines[-2].split('      ')[1:-1]
#     row_data = [s.strip() for s in row_data]
#     with open('results/results.csv', "a") as csvfile:
#         fieldnames = ['important features (n)', 'precision',
#                       'recall', 'f1-score', 'accuracy', 'run time']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerow({'important features (n)': num_of_features,
#                          'precision': row_data[0], 'recall': row_data[1], 'f1-score': row_data[2], 'accuracy': accuracy, 'run time': run_time})
#
#     with open('results/results.txt', 'a') as file:
#         file.write('\n#---------------------------------------------#\n')
#         file.write('\n' + report)
#         file.write('\naccuracy: ' + str(accuracy) + '%')
#         file.write('\nrun time: ' + str(run_time))
#         file.write('\nprobabilities:\n' + str(probabilities))
#         file.write('\ny_true: ' + str(y_true))
#         file.write('\ny_pred: ' + str(y_pred))
#         file.write('\nimportant features (n): ' + str(num_of_features))
#         file.write('\nfeature_importances:\n' + str(feature_importances))


def classify_authors(path_to_data, method):
    start_time = time.time()
    filenames, authors = get_filenames(path_to_data)
    accuracy = []
    # precision, recall, f1_score, accuracy = []
    # add_test_namespace(filenames)
    # if test_cpp_files(filenames):

    # X is a whole original dataset of samples
    # y is corresponding authors
    X = get_sample_matrix(filenames)
    y = authors

    if method == 'GradientBoostingClassifier':
        classifier = GradientBoostingClassifier()
    else:
        classifier = RandomForestClassifier(n_estimators=100, n_jobs=-1)

    kf = KFold(n_splits=10, shuffle=True)
    report = []
    for train_index, test_index in kf.split(X):
        X_train = X[train_index]
        y_train = y[train_index]
        classifier.fit(X_train, y_train)

        # cut unimportant features
        model = SelectFromModel(classifier, prefit=True)
        feature_usage = model.get_support()
        X_transformed = model.transform(X_train)
        classifier.fit(X_transformed, y_train)

        X_test = np.array([list(compress(sample, feature_usage)) for sample in X[test_index]])
        y_test = y[test_index]

        y_true = y_test
        y_pred = classifier.predict(X_test)

        fold_report = {'method': method,
                       'accuracy': accuracy_score(y_true, y_pred),
                       'precision': precision_score(y_true, y_pred, average='weighted'),
                       'recall': recall_score(y_true, y_pred, average='weighted'),
                       'f1-score': f1_score(y_true, y_pred, average='weighted'),
                       'run_time': round(time.time() - start_time, 2),
                       'feature importancies': get_feature_importances(classifier, feature_usage)}
        report.append(fold_report)

    with open('report.txt', 'w', encoding='utf-8') as outfile:
        json.dump(report, outfile, indent=4)
    return report


def get_feature_names(feature_usage):
    feature_names = ['ln_comments', 'ln_macros', 'ln_spaces', 'ln_tabs', 'ln_newlines', 'whitespace_ratio',
                     'lines_of_code', ]
    #  'ln_number_of_functions', 'avg_funcname_len', 'avg_varname_len', 'has_specialcharnames',
    #  'has_uppercasenames']
    keywords = re.split('[^a-z0-9_]+', open('./core/cpp_keywords.txt').read())
    feature_names += keywords
    feature_names = list(compress(feature_names, feature_usage))
    return feature_names


def get_feature_importances(classifier, feature_usage):
    importances = classifier.feature_importances_
    indices = np.argsort(importances)[:: -1]
    feature_names = get_feature_names(feature_usage)
    importances = sorted(importances, key=float, reverse=True)
    return list(zip([feature_names[i] for i in indices], importances))


# def get_oob_rate(X, y):
#     # calculate this on whole original set
#     ensemble_clfs = [
#         ("RandomForestClassifier, max_features='sqrt'",
#          RandomForestClassifier(warm_start=True, oob_score=True,
#                                 max_features="sqrt")),
#         ("RandomForestClassifier, max_features='log2'",
#          RandomForestClassifier(warm_start=True, max_features='log2',
#                                 oob_score=True)),
#         ("RandomForestClassifier, max_features=None",
#          RandomForestClassifier(warm_start=True, max_features=None,
#                                 oob_score=True))
#     ]
#
#     # Map a classifier name to a list of (<n_estimators>, <error rate>) pairs.
#     error_rate = OrderedDict((label, []) for label, _ in ensemble_clfs)
#     errors = OrderedDict((label, []) for label, _ in ensemble_clfs)
#
#     # Range of `n_estimators` values to explore.
#     min_estimators = 10
#     max_estimators = 100
#
#     for label, clf in ensemble_clfs:
#         for i in range(min_estimators, max_estimators + 1):
#             clf.set_params(n_estimators=i)
#             clf.fit(X, y)
#
#             # Record the OOB error for each `n_estimators=i` setting.
#             oob_error = 1 - clf.oob_score_
#             error_rate[label].append((i, oob_error))
#             errors[label].append(oob_error)
#
#     # Generate the "OOB error rate" vs. "n_estimators" plot.
#     for label, clf_err in error_rate.items():
#         xs, ys = zip(*clf_err)
#         plt.plot(xs, ys, label=label)
#         print(clf_err)
#
#     for label, clf_err in errors.items():
#         print(min(clf_err))
#
#     plt.xlim(min_estimators, max_estimators)
#     plt.xlabel("n_estimators")
#     plt.ylabel("OOB error rate")
#     plt.legend(loc="upper right")
#     plt.show()
