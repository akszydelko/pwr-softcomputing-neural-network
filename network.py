import numpy as np
import neurolab as nl


class LetterRecognitionNetwork(object):
    def __init__(self, alphabet):
        np_alphabet = np.asarray(alphabet, np.int)
        np_alphabet[np_alphabet == 0] = -1
        # for x in np_alphabet:
        #     print x
        self.network = nl.net.newhop(np_alphabet[:2], max_init=1000, delta=0)

    def what_is(self, letter):
        return np.asarray(self.network.sim([np.asarray(letter, np.int)]), np.int)

    def what_is_array(self, array):
        # for x in array:
        #     print x
        np_arr = np.asarray(array, np.int)
        np_arr[np_arr == 0] = -1
        return np.asarray(self.network.sim(np_arr), np.int)