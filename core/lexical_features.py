import re
import math


def get_lexical_features(filename):
    with open(filename, 'r') as in_file:
        lines = in_file.readlines()
        file_length = sum([len(line) for line in lines])

        if file_length != 0:
            avg_line_length = file_length / len(lines)

            # commenting style
            comments = len([line for line in lines if re.match(
                '(.*)//', line) or re.match('(.*)/\*', line)])
            inline_comments = len([line for line in lines if re.match('(.*)//', line)])
            multiline_comments = len(
                [line for line in lines if re.match('(.*)/\*', line)])

            # layout
            newlines = sum([line.count('\n') for line in lines])
            spaces = sum([line.count(' ') for line in lines])
            tabs = sum([line.count('\t') for line in lines if not (
                line.startswith('char') or line.startswith('string'))])
            macros = len([line for line in lines if re.search('#define .*.\(.*\)', line)])

            # bracing style
            open_brace_alone = len(
                [line for line in lines if re.match('^([\s\t\n]*)\{([\s\t\n]*)$', line)])
            open_brace_first = len([line for line in lines if re.match('^\{(.*?)', line)])
            open_brace_last = len([line for line in lines if re.match('^(.*?)\{$', line)])
            closing_brace_alone = len(
                [line for line in lines if re.match('^([\s\t\n]*)\}([\s\t\n]*)$', line)])
            closing_brace_first = len([line for line in lines if re.match('^\}(.*?)', line)])
            closing_brace_last = len([line for line in lines if re.match('^(.*?)\}$', line)])

            ln_open_brace_alone = math.log(
                open_brace_alone / file_length) if open_brace_alone else 0
            ln_open_brace_first = math.log(
                open_brace_first / file_length) if open_brace_first else 0
            ln_open_brace_last = math.log(
                open_brace_last / file_length) if open_brace_last else 0
            ln_closing_brace_alone = math.log(
                closing_brace_alone / file_length) if closing_brace_alone else 0
            ln_closing_brace_first = math.log(
                closing_brace_first / file_length) if closing_brace_first else 0
            ln_closing_brace_last = math.log(
                closing_brace_last / file_length) if closing_brace_last else 0

            ln_comments = math.log(comments / file_length) if comments else 0
            ln_inline_comments = math.log(
                inline_comments / file_length) if inline_comments else 0
            ln_multiline_comments = math.log(
                multiline_comments / file_length) if multiline_comments else 0
            ln_spaces = math.log(spaces / file_length) if spaces else 0
            ln_tabs = math.log(tabs / file_length) if tabs else 0
            ln_newlines = math.log(newlines / file_length) if newlines else 0
            ln_macros = math.log(macros / file_length) if macros else 0
            lines_of_code = len([line for line in lines if line.strip(' \n') != ''])
            whitespace_ratio = (spaces + tabs + newlines) / file_length

            lexical_features = [ln_comments, ln_inline_comments, ln_multiline_comments,
                                ln_macros, ln_spaces, ln_tabs, ln_newlines, whitespace_ratio,
                                lines_of_code, avg_line_length,
                                ln_open_brace_alone, ln_open_brace_first, ln_open_brace_last,
                                ln_closing_brace_alone, ln_closing_brace_first, ln_closing_brace_last]
            return lexical_features
        else:
            pass
