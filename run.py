import argparse
import os
import pickle

from numpy import ndarray, asarray, set_printoptions

from network import LetterRecognitionNetworkBase, LetterRecognitionNetwork
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
    parser.add_argument("-an", "--analyze", help="Create analytics file.", action="store_true")
    parser.add_argument("-ac", "--alphabetCoded", help="Coded Alphabet file, have to be used with -a.")
    parser.add_argument("-un", "--useNetwork", help="Path to pickle file with network object to use.")
    parser.add_argument("-sn", "--saveNetwork", help="Save used network to given file.")
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
    alphabet = utils.read_coded_alphabet(ALPHABET_CODED)
    alphabet_bin = utils.get_bin_coded_data(utils.read_coded_alphabet(ALPHABET_CODED))
    display_alphabet = utils.read_alphabet(ALPHABET)

    if hasattr(args, 'useNetwork') and args.useNetwork:
        with open(args.useNetwork, 'r') as f:
            network = pickle.load(f)
    else:
        # Create network
        network = LetterRecognitionNetwork(
            utils.BINARY_MATRIX_SIZE * utils.BINARY_MATRIX_SIZE * utils.BIN_EDGE_ARRAY_SIZE,
            180,
            len(display_alphabet)
        )

        # Add learning data and train the network
        learning_iterations = 180
        network\
            .add_learning_data(alphabet_bin, display_alphabet)\
            .train(learning_iterations, learningrate=0.05, momentum=0.1, weightdecay=0.01, lrdecay=1.0)

        if hasattr(args, 'saveNetwork') and args.saveNetwork:
            with open(args.saveNetwork, 'wb') as f:
                pickle.dump(network, f)

    # Use network to recognise message
    coded_message = utils.read_coded_massage(file_path)
    coded_message_bin = utils.get_bin_coded_data(coded_message)
    print '----------------------------------------\n\n'
    print '### Recognized message:'
    real_message = utils.get_test_original_massage(TESTS[args.test + '_original'].strip().lower()).strip()
    message = network.read_data_set(coded_message_bin).strip().lower()
    cap_step_1 = '. '.join([x.capitalize() for x in message.split('. ')])
    cap_step_2 = '\n'.join([x[0].capitalize() + x[1:] if len(x) > 1 else x for x in cap_step_1.split('\n')])
    print cap_step_2

    if hasattr(args, 'test') and args.test and hasattr(args, 'original') and args.original:
        print '\n### Original message:'
        real_message = utils.get_test_original_massage(TESTS[args.test + '_original'].strip().lower()).strip()
        print real_message
        good_recognition_count = sum(message[i] == real_message[i].lower() for i in xrange(len(real_message)))
        print '\n\nGood recognition:\n%d%%\t%d/%d characters' % (
            100 * good_recognition_count / len(real_message), good_recognition_count, len(real_message))

        if hasattr(args, 'analyze') and args.analyze:
            options_mapping = {
                'learningrate': 'Learning rate',
                'momentum': 'Momentum',
                'weightdecay': 'Weight decay rate',
                'lrdecay': 'Learning decay rate'
            }

            with open(os.path.join(os.path.dirname(__file__), 'analytics', TESTS[args.test]), 'wb') as f:
                print >> f, 'Network:'
                print >> f, 'Input layer:', network.layers[0]
                print >> f, 'Hidden layer:', network.layers[1]
                print >> f, 'Output layer:', network.layers[2]

                print >> f, '\nLearning options:'
                for key in network.learning_options:
                    print >> f, '%s: %s' % (options_mapping.get(key, key), network.learning_options[key])

                print >> f, '\nEpoches:', network.trainer.totalepochs
                print >> f, 'Total Error:', network.total_error
                print >> f, 'Good recognition: %d%% - %d/%d characters' % (
                    100 * good_recognition_count / len(real_message), good_recognition_count, len(real_message))
                print >> f, '\n### Recognized message:'
                print >> f, cap_step_2
                print >> f, '\n### Original message:'
                print >> f, real_message

                set_printoptions(linewidth=100)
                real_message = real_message.replace('\r', '')
                message = message.replace('\r', '')

                for i, sample in enumerate(coded_message_bin):
                    if isinstance(sample, ndarray):
                        print >> f, '\n\n----------------------------------------------------------'
                        print >> f, 'Expected:', real_message[i]
                        print >> f, 'Got:', message[i]
                        print >> f, 'WRONG!' if real_message[i].lower() != message[i] else 'OK'

                        print >> f, '\nCoded letter:'
                        print >> f, asarray(utils.codded_array_to_matrix(coded_message[i]))

                        original_expected_letter_index = display_alphabet.index(real_message[i].upper())
                        print >> f, '\nOriginal expected letter:'
                        print >> f, asarray(utils.codded_array_to_matrix(alphabet[original_expected_letter_index]))

                        original_got_letter_index = display_alphabet.index(message[i].upper())
                        print >> f, '\nOriginal got letter:'
                        print >> f, asarray(utils.codded_array_to_matrix(alphabet[original_got_letter_index]))

                        print >> f, '\nBin coded letter:'
                        print >> f, sample

                        print >> f, '\nBin original expected letter:'
                        print >> f, alphabet_bin[original_expected_letter_index]

                        print >> f, '\nBin original got letter:'
                        print >> f, alphabet_bin[original_got_letter_index]