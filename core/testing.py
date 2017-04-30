from core import syntactic_features


def test_cpp_files(filenames):
    """
    Testing if all of the cpp-files are compilable
    by parsing with gccXML/pygccxml
    and extracting syntactic_features
    """
    for filename in filenames:
        syntactic_features.get_syntactic_features(filename)
    return True


def add_test_namespace(filenames):
    """
    Adding namespace test{...} into all cpp-files.
    Otherwise pygccxml will not extract any syntactic features.
    """
    for file in filenames:
        # file = "tmp/example.cpp"
        with open(file, "r", encoding='utf-8', errors='ignore') as in_file:
            buf = in_file.readlines()
            already_inserted = False
            for line in buf:
                if 'namespace test {' in line:
                    already_inserted = True
            if already_inserted == False:
                with open(file, "w") as out_file:
                    for line in buf:
                        # TODO: re-write using regex?
                        if not (line.startswith('#') or line.startswith(' ') or line.startswith(
                                '*') or line.startswith('\\') or line.startswith('\n') or line.startswith(
                                '\t') or line.startswith('/')) and already_inserted == False:
                            line = line + "\nnamespace test {\n"
                            already_inserted = True
                        out_file.write(line)
                with open(file, "a") as out_file:
                    out_file.write('}')
