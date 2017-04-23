import re
import math

def get_lexical_features(filename):
    with open(filename, 'r') as in_file:
        lines = in_file.readlines()
        file_length = sum([len(line) for line in lines])
        if file_length != 0:
            comments = len([line for line in lines if re.match('(.*)//', line) or re.match('(.*)/\*', line)])
            newlines = sum([line.count('\n') for line in lines])
            spaces = sum([line.count(' ') for line in lines])
            tabs = sum([line.count('\t') for line in lines if not (line.startswith('char') or line.startswith('string'))])
            macros = len([line for line in lines if re.search('#define .*.\(.*\)', line)])

            ln_comments = math.log(comments / file_length) if comments else 0
            ln_spaces = math.log(spaces / file_length) if spaces else 0
            ln_tabs = math.log(tabs / file_length) if tabs else 0
            ln_newlines = math.log(newlines / file_length) if newlines else 0
            ln_macros = math.log(macros / file_length) if macros else 0
            lines_of_code = len([line for line in lines if line.strip(' \n') != ''])
            whitespace_ratio = (spaces + tabs + newlines) / file_length

            lexical_features = [ln_comments, ln_macros, ln_spaces, ln_tabs, ln_newlines, whitespace_ratio, lines_of_code]
            return lexical_features
    return None