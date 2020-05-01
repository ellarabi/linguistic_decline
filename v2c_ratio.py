
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

epitran_model = sys.argv[1] # epitran model to generate transliterations
declining_file = sys.argv[2] # text file with declining words, one per line
stable_file = sys.argv[3] # text file with stable words, one per line

epi = epitran.Epitran(epitran_model)

def fix_nasals_transcription(word, transcription):
    valid_type = False
    elements = re.findall(vnnnc, word, overlapped=True)
    for e in elements:
        if word.endswith(e): valid_type = True
    if not valid_type:
        return transcription

    transcription_new = ''
    if word.endswith('ement'):  transcription_new = re.sub('ɛm$', 'mâ', transcription)
    elif word.endswith('ment'): transcription_new = re.sub('m$', 'mâ',  transcription)
    elif word.endswith('ent'): transcription_new = transcription
    elif len(re.findall(vnmeot, transcription)) > 0:
        transcription_new = transcription[:-1]
        current = transcription_new[-1]  # the last vowel
        transcription_new = transcription_new[:-1] + mapping.get(current, current)
    else:
        transcription_new = transcription

    return transcription_new

def list_vtcr(words):
    vowels = "ɪøæoiəeɑoaɛɔuʌʊâyœ̃ɔ̃œɛ̃ə̃âɛ̃ɔ̃"
    l = []
    for word in words:
        sounds = epi.transliterate(word, ligatures = True)
#		Special handling for French
#       sounds = fix_nasals_transcription(word, sounds)
        v = 0
        c = 0
        for sound in sounds:
            if sound in "ɛ̃" and sound in "ə̃":
                v += 0
            elif sound in "ː":
                c += 0
            elif sound in vowels:
                v += 1
            else:
                c += 1
        l.append(v / c)
    return l

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

f = open(declining_file, "r")

decl = [line.strip() for line in f]

f = open(stable_file, "r")

stable = [line.strip() for line in f]

d1 = list_vtcr(decl)
d2 = list_vtcr(stable)

compare_distributions(d1, d2)