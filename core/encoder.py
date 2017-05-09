import os


def file_is_empty(path):
    return os.stat(path).st_size == 0


def correctEncoding(filename, encoding_from="ISO-8859-14", encoding_to='UTF-8'):
    if not file_is_empty(filename):
        with open(filename, 'r', encoding=encoding_from) as fr:
            with open('./tmp/decoded.cxx', 'w', encoding=encoding_to) as fw:
                for line in fr:
                    fw.write(line[:-1] + '\r\n')

        os.remove(filename)

        with open('./tmp/decoded.cxx', 'r') as fr:
            with open(filename, 'w', encoding=encoding_to) as fw:
                for line in fr:
                    fw.write(line[:-1] + '\r\n')
    else:
        print('Removing empty file...')
        os.remove(filename)
