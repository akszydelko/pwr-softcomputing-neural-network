from numpy import asarray, ndarray
from pybrain.structure import RecurrentNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork

import utils as my_utils


class DataError(Exception):
    pass


class LetterRecognitionNetworkBase(object):
    layers = []
    training_data = None
    test_data = None
    total_error = None
    trainer = None
    learning_options = {}

    def __init__(self, in_layer_size, hidden_layer_size, out_layer_size):
        """Creates network with layers and all connections."""
        self.input_size = in_layer_size
        self.layers = (self.input_size, hidden_layer_size, out_layer_size)
        self.network = self._create_network(*self.layers)

    def _create_network(self, in_layer_size, hidden_layer_size, out_layer_size):
        """Creates and return a network based on self._network_class class."""
        return buildNetwork(in_layer_size, hidden_layer_size, out_layer_size,
                            hiddenclass=SigmoidLayer, outclass=LinearLayer, recurrent=True,
                            bias=False, outputbias=True)

    def add_learning_data(self, data, data_labels):
        """Add and classify data for the training procedure and for recognitions queries."""
        if len(data) != len(data_labels):
            raise DataError("Number of data inputs has to be equal with number of data labels.")

        self.training_data = ClassificationDataSet(self.input_size, nb_classes=len(data_labels), class_labels=data_labels)

        print "\n----------------------------------------"
        print "Training procedure:"
        for i, letter in enumerate(data):
            sample = asarray(letter, dtype='int64').reshape(self.input_size, 1)
            self.training_data.addSample(sample[:, 0], i)

        self.test_data, _ = self.training_data.splitWithProportion(.6)

        self.training_data._convertToOneOfMany()
        self.test_data._convertToOneOfMany()

        return self

    def check_learning_results(self):
        """Test network on the part of learning data."""
        out = self.network.activateOnDataset(self.test_data)
        out = out.argmax(axis=1)  # the highest output activation gives the class

        test_case = self.test_data['class'][:, 0]

        print "\n----------------------------------------"
        print "Testing charset:\n" + str([self.training_data.getClass(int(i)) for i in test_case])

        recognized_letters = []
        for e in out:
            recognized_letters.append(self.training_data.getClass(int(e)))

        print "Recognized charset:\n" + str(recognized_letters)

        percent = 0
        for i, recognized_letter in enumerate(recognized_letters):
            if recognized_letter == self.training_data.getClass(int(test_case[i])):
                percent += 1

        print "\n%d %% Recognized" % (percent * (100. / len(test_case)))

    def train(self, iterations, trainer_class=BackpropTrainer, **kwargs):
        """Run the learning procedure."""
        self.learning_options.update(kwargs or {})
        self.trainer = trainer_class(self.network, dataset=self.training_data, **self.learning_options)

        # training iterations
        for i in xrange(iterations):
            self.total_error = self.trainer.train()
            if (i+1) % 20 == 0 or i+1 == iterations:
                print "%2d%%\tEpoches: %4d/%d\tTotal error:%f" % \
                      (100*self.trainer.totalepochs/iterations, self.trainer.totalepochs, iterations, self.total_error)

    def read_data_set(self, data):
        """Run the module's forward pass on the given dataset unconditionally
            and return the output."""
        self.network.reset()
        out = []
        for i, sample in enumerate(data):
            if isinstance(sample, ndarray):
                _sample = asarray(sample, dtype='int64').reshape(self.input_size, 1)[:, 0]
                out.append(self.network.activate(_sample).argmax())
            else:
                out.append(sample)
        self.network.reset()

        return ''.join([self.training_data.getClass(int(x)) if isinstance(x, int) else x for x in out])


class LetterRecognitionNetwork(LetterRecognitionNetworkBase):
    _network_class = RecurrentNetwork

    def __init__(self, in_layer_size, hidden_layer_size, out_layer_size):
        super(LetterRecognitionNetwork, self).__init__(in_layer_size, hidden_layer_size, out_layer_size)

        self._create_layers(in_layer_size, hidden_layer_size, out_layer_size)
        self._add_connections()

        self.network.sortModules()

    def _create_network(self, *args):
        """Creates and return a network based on self._network_class class."""
        return self._network_class()

    def _create_layers(self, in_layer_size, hidden_layer_size, out_layer_size, hidden_layer_class=SigmoidLayer):
        """Creates three layers: input, hidden and output. Then adds them to the network instance."""
        self.network.addInputModule(LinearLayer(in_layer_size, name='in'))
        self.network.addModule(hidden_layer_class(hidden_layer_size, name='hidden'))
        self.network.addOutputModule(LinearLayer(out_layer_size, name='out'))

    def _add_connections(self):
        """Creates and adds connections between layers in the network instance."""
        self.network.addConnection(FullConnection(self.network['in'], self.network['hidden'], name='c1'))
        self.network.addConnection(FullConnection(self.network['hidden'], self.network['out'], name='c2'))
        self.network.addRecurrentConnection(FullConnection(self.network['hidden'], self.network['hidden'], name='c3'))


if __name__ == '__main__':
    # Simple network test
    alphabet_bin = my_utils.get_bin_coded_data(my_utils.read_coded_alphabet('alfabet_codificat.txt'))
    alphabet = my_utils.read_alphabet('alfabet.txt')

    n = LetterRecognitionNetworkBase(10*10*3, 26, 26)
    n.add_learning_data(alphabet_bin, alphabet).train(240)

    n.check_learning_results()
    print n.read_data_set(alphabet_bin)
