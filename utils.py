import os

import numpy


BINARY_MATRIX_SIZE = 10
BIN_EDGE_ARRAY_SIZE = 3


def get_file_path_data(file_name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', file_name)


def get_file_path_tests(file_name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/test_cases', file_name)


def read_coded_alphabet(file_name):
    """Read coded alphabet from the file."""
    out = []
    with open(get_file_path_data(file_name), 'r') as reader:
        for line in reader:
            out += [[int(x) for x in line.strip().split(' ')]]

    return out


def read_alphabet(file_name):
    """Read alphabet from the file."""
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
    # print file_list
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
                # line_numbers = line[1:].strip().split(' ')
                # out += [[[int(line_numbers.pop(0)) for x in xrange(int(line[0]))] for raw in xrange(int(line[0]))]]
                # print out

    return out


def codded_array_to_matrix(array):
    line_numbers = array[1:]
    return [[int(line_numbers.pop(0)) for col in xrange(int(array[0]))] for raw in xrange(int(array[0]))]


def original_from_matrix(matrix):
    out = [len(matrix)]
    return out + [col for raw in matrix for col in raw]


def get_test_original_massage(file_name):
    with open(get_file_path_tests(file_name), 'r') as f:
        return f.read()


def convert_int_to_bin_array(number, size=BIN_EDGE_ARRAY_SIZE):
    bin_value = [int(x) for x in bin(number)[2:]]

    if len(bin_value) > size:
        raise IOError("Given number is too big to fit in binary representation with max length %s" % size)

    while len(bin_value) < size:
        bin_value = [0] + bin_value

    return bin_value


def form_binary_matrix(matrix):
    matrix = numpy.asarray(matrix, numpy.int)
    out_matrix = numpy.zeros(
        (BINARY_MATRIX_SIZE, BINARY_MATRIX_SIZE * BIN_EDGE_ARRAY_SIZE), numpy.int)

    for i in xrange(len(matrix)):
        for q in xrange(len(matrix[i])):
            out_matrix[i][q * BIN_EDGE_ARRAY_SIZE: q * BIN_EDGE_ARRAY_SIZE + BIN_EDGE_ARRAY_SIZE] = \
                convert_int_to_bin_array(matrix[i][q])

    return out_matrix


def make_matrix_flat(matrix):
    out = numpy.zeros(BINARY_MATRIX_SIZE * BINARY_MATRIX_SIZE * BIN_EDGE_ARRAY_SIZE, numpy.int)
    for i in xrange(len(matrix)):
        out[i * BINARY_MATRIX_SIZE * BIN_EDGE_ARRAY_SIZE:
            i * BINARY_MATRIX_SIZE * BIN_EDGE_ARRAY_SIZE + BINARY_MATRIX_SIZE * BIN_EDGE_ARRAY_SIZE] = \
            matrix[i]

    return out


def get_bin_coded_alphabet(alphabet):
    return [form_binary_matrix(codded_array_to_matrix(letter_array)) for letter_array in alphabet]


def get_bin_coded_alphabet_flat(alphabet):
    return [make_matrix_flat(form_binary_matrix(codded_array_to_matrix(letter_array))) for letter_array in alphabet]
