from pygccxml import utils, declarations, parser
import re
import math

import logging

logging.basicConfig(filename='./tmp/test.log',
                    filemode='w', level=logging.DEBUG)


def get_avg_funcname_len(namespace):
    avg_funcname_len = 0
    free = namespace.free_functions(allow_empty=True)
    member = namespace.member_functions(allow_empty=True)
    number_of_functions = len(free) + len(member)
    if number_of_functions != 0:
        avg_funcname_len = (sum([len(func.name) for func in free]) +
                            sum([len(func.name) for func in member])) / number_of_functions
    return avg_funcname_len


def get_avg_varname_len(namespace):
    avg_varname_len = 0
    vars = namespace.variables(allow_empty=True)
    number_of_vars = len(vars)
    if number_of_vars != 0:
        avg_varname_len = sum(len(var.name) for var in vars) / number_of_vars
    return avg_varname_len


def check_specialcharnames(namespace):
    has_specialcharnames = 0
    decls = namespace.declarations
    if len([decl for decl in decls if re.search('[^A-Za-z0-9_]+.*', decl.name)]) != 0:
        has_specialcharnames = 1
    return has_specialcharnames


def check_uppercasenames(namespace):
    vars = namespace.variables(allow_empty=True)
    free = namespace.free_functions(allow_empty=True)
    members = namespace.member_functions(allow_empty=True)
    if False in [var.name.islower() for var in vars] or [func.name.islower() for func in free] or [func.name.islower() for func in members]:
        return 1
    return 0


def get_syntactic_features(filename):
    try:
        # Find the location of the xml generator (castxml or gccxml)
        generator_path, generator_name = utils.find_xml_generator()
        # Configure the xml generator
        xml_generator_config = parser.xml_generator_configuration_t(
            xml_generator_path=generator_path,
            xml_generator=generator_name)
        # Parse the c++ file
        decls = parser.parse([filename], xml_generator_config)
        global_namespace = declarations.get_global_namespace(decls)

        namespace = global_namespace.namespace("test")

        with open(filename, 'r') as in_file:
            lines = in_file.readlines()
            file_length = sum([len(line) for line in lines])

        number_of_functions = len(namespace.free_functions(allow_empty=True)) + \
            len(namespace.member_functions(allow_empty=True))
        ln_number_of_functions = math.log(
            number_of_functions / file_length) if number_of_functions else 0
        avg_funcname_len = get_avg_funcname_len(namespace)
        avg_varname_len = get_avg_varname_len(namespace)
        has_specialcharnames = check_specialcharnames(namespace)
        has_uppercasenames = check_uppercasenames(namespace)

        syntactic_features = [ln_number_of_functions, avg_funcname_len,
                              avg_varname_len, has_specialcharnames, has_uppercasenames]
        # logging.info('OK')
        return syntactic_features
    except:
        logging.debug('Compilation test failed.')
