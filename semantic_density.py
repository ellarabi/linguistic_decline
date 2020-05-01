
import math
import pickle
import scipy.stats
import numpy
import scipy.linalg
import eng_to_ipa as ipa
import polyglot
from polyglot.text import Text, Word
import random
import epitran
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import statsmodels.api as sm

def pickle_dictionary(numpy_file, vocab_file, target_pickle):
    a = numpy.load(numpy_file)

    f = open(vocab_file, "rb")

    v = pickle.load(f)

    f.close()

    d = {}

    for i in range(0, len(v)):
        d[v[i]] = a[i]

    f = open(target_pickle, "wb")

    pickle.dump(d, f)

    f.close()

def retrieve_dictionary(filename):

    f = open(filename, "rb")

    d = pickle.load(f)

    f.close()

    return d

def similarity(d, wa, wb):
    va = d[wa]
    vb = d[wb]
    na = numpy.linalg.norm(va)
    nb = numpy.linalg.norm(vb)
    do = numpy.dot(va, vb)
    if na == 0 or nb == 0:
        return 0
    return do / (na * nb)

def nearest_neighbours(d, word, n):
    l = []
    for comp in d:
        if comp != word:
            l.append((comp, similarity(d, word, comp)))

    l.sort(key = lambda el: el[1], reverse = True)

    return [x[0] for x in l[0:n]]

def semantic_density(d, word, n):
    nb = nearest_neighbours(d, word, n)

    sims = [similarity(d, x, word) for x in nb]

    return sum(sims) / n

def list_densities_nn(d, words, n):
    densities = []

    for word in words:
        if word in d:
            densities.append(semantic_density(d, word, n))
        else:
            densities.append(0)

    return densities

def compare_distributions(d1, d2):
    print("mean (declining)")
    print(numpy.mean(d1))
    print("mean (stable)")
    print(numpy.mean(d2))
    print("std (declining)")
    print(numpy.std(d1))
    print("std (stable)")
    print(numpy.std(d2))
    print("Mann-Whitney rank test")
    print(scipy.stats.mannwhitneyu(d1, d2, alternative="two-sided"))


numpy_file = sys.argv[1] # filename of numpy file (from Hamilton & Jurafsky SGNS data)
vocab_file = sys.argv[2] # filename of vocab file (from Hamilton & Jurafsky SGNS data)
pickle_filename = sys.argv[3] # filename for intermediate pickled dictionary to be stored
declining_file = sys.argv[4] # text file with declining words, one per line
stable_file = sys.argv[5] # text file with stable words, one per line

try:
	d = retrieve_dictionary(pickle_filename)
except IOError:
	pickle_dictionary(numpy_file, vocab_file, pickle_filename)
	d = retrieve_dictionary(pickle_filename)

f = open(declining_file, "r")

decl = [line.strip() for line in f]

f = open(stable_file, "r")

stable = [line.strip() for line in f]

d1 = list_densities_nn(d, decl, 10)
d2 = list_densities_nn(d, stable, 10)

densities = {}

for i in range(len(decl)):
    densities[decl[i]] = d1[i]
    densities[stable[i]] = d2[i]

num = 0
total = 0
for word in decl + stable:
    if word in d and max(d[word]) > 0.0000000001:
        num += 1
        total += densities[word]

avg = total / num

for word in decl + stable:
    if word not in d or max(d[word]) < 0.00000000001:
        densities[word] = avg
    print(word + "," + str(densities[word]))

for i in range(len(decl)):
    d1[i] = densities[decl[i]]
    d2[i] = densities[stable[i]]

compare_distributions(d1, d2)