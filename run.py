import argparse
import os
from network import LetterRecognitionNetwork
import utils
import numpy as np


TESTS = {
    't1': 'text_1.txt', 't1_original': 'text_1_chars.txt',
    't2': 'text_2.txt', 't2_original': 'text_2_chars.txt',
    't3': 'text_3.txt', 't3_original': 'text_3_chars.txt',
    't4': 'text_4.txt', 't4_original': 'text_4_chars.txt',
    't5': 'text_5.txt', 't5_original': 'text_5_chars.txt',
    't6': 'text_6.txt', 't6_original': 'text_6_chars.txt'
}

ALPHABET = 'alfabet.txt'
ALPHABET_CODED = 'alfabet_codificat.txt'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Letter recognition process.')
    #parser.add_argument("-t", "--test", help="Test number from 1-6. Eg. -t t2.")
    #parser.add_argument("-o", "--original", help="print original massage. ONLY when use -t.", action="store_true")
    parser.add_argument("-p", "--path", help="Path to file with coded massage.")
    parser.add_argument("-a", "--alphabet", help="Alphabet file, have to be used with -ac.")
    parser.add_argument("-ac", "--alphabetCoded", help="Coded Alphabet file, have to be used with -a.")
    args = parser.parse_args()

    if hasattr(args, 'alphabet') and args.alphabet and hasattr(args, 'alphabetCoded') and args.aplhabetCoded:
        ALPHABET = args.alphabet
        ALPHABET_CODED = args.aplhabetCoded

    file_path = utils.get_file_path_tests(TESTS['t1'])

    if hasattr(args, 'test') and args.test:
        file_path = utils.get_file_path_tests(TESTS[args.test])
    elif hasattr(args, 'path') and args.path:
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), args.path)

    display_alphabet = utils.read_alphabet(ALPHABET)

    # TODO: 1. Train the network
    # Create network
    alphabet_bin = utils.get_bin_coded_alphabet_flat(utils.read_coded_alphabet(ALPHABET_CODED))
    network = LetterRecognitionNetwork(alphabet_bin)
    # TODO: 2. Use network to recognise message
    al = np.asarray(alphabet_bin, np.int)
    al[al == 0] = -1
    result = network.what_is_array(al)
    # print("Test on train samples:")
    # for i in xrange(len(al)):
    #     print display_alphabet[i], (result[i] == al[i]).all()

    # --- Coded text check ----------------------------------------------------------------
    arr = utils.read_coded_massage(file_path)
    arr_bin = []
    for letter in arr:
        if isinstance(letter, list):
            arr_bin += [utils.make_matrix_flat(utils.form_binary_matrix(utils.codded_array_to_matrix(letter)))]

    arr_bin = np.asarray(arr_bin, np.int)

    arr_bin[arr_bin == 0] = -1
    result = network.what_is_array(arr_bin)
    print 'Testing simple text:'
    for i in xrange(len(result)):
        for q in xrange(len(al)):
            if (result[i] == al[q]).all():
                print display_alphabet[q],
    # --- End coded text check ----------------------------------------------------------------

    if hasattr(args, 'test') and args.test and hasattr(args, 'original') and args.original:
        print '\n Original massage:'
        print utils.get_test_original_massage(TESTS[args.test + '_original'].strip().lower())

