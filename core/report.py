

class Report:

    def __init__(self, classifier, sample_matrix):
        self.classifier = classifier

    def say_hello():
        return 'hello'

    hello = say_hello()


class SamlpeMatrix:

    def get_filenames():
        filenames_list = np.array([])
        authors = np.array([])
        for dirpath, dirnames, filenames in os.walk(self.path_to_data):
            for filename in [f for f in filenames if f.endswith(".cpp")]:
                authors = np.append(authors, os.path.basename(dirpath))
                filenames_list = np.append(filenames_list, os.path.join(dirpath, filename))
        return filenames_list, authors

    filenames, authors = get_filenames(self.path_to_data)
    lexical_features = [get_lexical_features(filename) for filename in filenames]
    syntactic_features = [get_syntactic_features(filename) for filename in filenames]
    keywords = count_cppkeywords_tf(filenames)
    all_features = np.hstack((lexical_features, syntactic_features, keywords))

    def __init__(self, path_to_data):
        self.path_to_data = path_to_data
