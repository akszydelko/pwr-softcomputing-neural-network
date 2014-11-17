from numpy import *
from pybrain.structure import *
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
import utils as my_utils


LETTER_SIZE = 10 * 10 * 3

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']

ALPHABET_SIZE = len(alphabet)

# ----------------------------------------

trnData = ClassificationDataSet(LETTER_SIZE, 1, nb_classes=len(alphabet), class_labels=alphabet)

alphabet_bin = my_utils.get_bin_coded_alphabet_flat(my_utils.read_coded_alphabet('alfabet_codificat.txt'))

for i, letter in enumerate(alphabet_bin):
    trnData.addSample(asarray(letter), [i])

tstData, _ = trnData.splitWithProportion(1.0)

trnData._convertToOneOfMany()
tstData._convertToOneOfMany()

# creating network
n = RecurrentNetwork()

# creating layers and adding layers to the net
n.addInputModule(LinearLayer(LETTER_SIZE, name='in'))
n.addModule(SigmoidLayer(ALPHABET_SIZE, name='hidden'))
n.addOutputModule(LinearLayer(ALPHABET_SIZE, name='out'))

# creating connections & adding connections to the network
n.addConnection(FullConnection(n['in'], n['hidden'], name='c1'))
n.addConnection(FullConnection(n['hidden'], n['out'], name='c2'))
n.addRecurrentConnection(FullConnection(n['hidden'], n['hidden'], name='c3'))

# making MLP usable
n.sortModules()

trainer = BackpropTrainer(n, dataset=trnData, momentum=0.1, verbose=False, weightdecay=0.01)

# training iterations
for i in range(40):
    trainer.trainEpochs(20)
    print "epoch: %4d" % trainer.totalepochs


# outs
out = n.activateOnDataset(tstData)
out = out.argmax(axis=1)  # the highest output activation gives the class

# ----------------------------------------

test_case = tstData['class'][:, 0]

alphabet_test = []
for e in test_case:
    alphabet_test.append(alphabet[int(e)])

print "----------------------------------------"
print "Testowane znaki:\n" + str(alphabet_test)

recognized_letters = []
for e in out:
    recognized_letters.append(alphabet[int(e)])

print "Rozpoznane znaki:\n" + str(recognized_letters)

percent = 0
for i in range(0, len(alphabet_test)):
    if alphabet_test[i] == recognized_letters[i]:
        percent += 1.

print "%d %% Recognized" % (percent * (100. / len(alphabet_test)))
