import argparse
import os

from network import LetterRecognitionNetworkBase
import utils


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
    parser.add_argument("-t", "--test", help="Test number from 1-6. Eg. -t t2.")
    parser.add_argument("-o", "--original", help="print original massage. ONLY when use -t.", action="store_true")
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

    # Load alphabet
    alphabet_bin = utils.get_bin_coded_data(utils.read_coded_alphabet(ALPHABET_CODED))
    display_alphabet = utils.read_alphabet(ALPHABET)

    # Create network
    network = LetterRecognitionNetworkBase(
        utils.BINARY_MATRIX_SIZE * utils.BINARY_MATRIX_SIZE * utils.BIN_EDGE_ARRAY_SIZE,
        len(display_alphabet),
        len(display_alphabet)
    )

    # Add learning data and train the network
    network.add_learning_data(alphabet_bin, display_alphabet).train(200)

    # Use network to recognise message
    coded_message = utils.get_bin_coded_data(utils.read_coded_massage(file_path))
    print '----------------------------------------\n\n'
    print '### Recognized message:'
    message = network.read_data_set(coded_message).lower()
    cap_step_1 = '. '.join([x.capitalize() for x in message.split('. ')])
    cap_step_2 = '\n'.join([x[0].capitalize() + x[1:] if len(x) > 1 else x for x in cap_step_1.split('\n')])
    print cap_step_2

    if hasattr(args, 'test') and args.test and hasattr(args, 'original') and args.original:
        print '### Original message:'
        real_message = utils.get_test_original_massage(TESTS[args.test + '_original'].strip().lower())
        print real_message
        good_recognition_count = sum(message[i] == real_message[i].lower() for i in xrange((len(real_message))))
        print '\n\nGood recognition:\n%d%%\t%d/%d characters' % (
            100 * good_recognition_count / len(real_message), good_recognition_count, len(real_message))
