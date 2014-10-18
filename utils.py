import os


def get_file_path_data(file_name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', file_name)

def get_file_path_tests(file_name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/test_cases', file_name)

def read_coded_alphabet(file_name):
    '''Read coded alphabet from the file.'''
    out = []
    with open(get_file_path_data(file_name), 'r') as reader:
        for line in reader:
            out += [[int(x) for x in line.strip().split(' ')]]

    return out

def read_alphabet(file_name):
    '''Read alphabet from the file.'''
    out = []
    with open(get_file_path_data(file_name), 'r') as reader:
        for line in reader:
            out += [line.strip()]

    return out

def get_tests_list():
    file_list = []
    for f in os.listdir("tests/test_cases"):
        file_list += [f]
    file_list = sorted(file_list)
    #print file_list
    out = [(get_file_path_tests(a), get_file_path_tests(file_list[file_list.index(a) + 1])) for a in file_list[::2]]

    return out

def read_coded_massage(file_name):
    out = []
    with open(file_name, 'r') as reader:
        for line in reader:
            if len(line.strip()) < 3:
                # Special char
                try:
                    out += [int(line.strip())]
                except ValueError:
                    # not recognized char
                    out += [str(line)]
            else:
                out += [[int(x) for x in line.strip().split(' ')]]
                #line_numbers = line[1:].strip().split(' ')
                #out += [[[int(line_numbers.pop(0)) for x in xrange(int(line[0]))] for raw in xrange(int(line[0]))]]
            #print out

    return out

def matrix_form(array):
    line_numbers = array[1:]
    return [[int(line_numbers.pop(0)) for col in xrange(int(array[0]))] for raw in xrange(int(array[0]))]


def original_from_matrix(matrix):
    out = [len(matrix)]
    return out + [col for raw in matrix for col in raw]


def get_test_original_massage(file_name):
    with open(get_file_path_tests(file_name), 'r') as f:
        return f.read()
