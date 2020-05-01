import pickle
import spacy

nlp_model = sys.argv[1]   # Name of a spacy model e.g. fre_core_news_sm
source_file = sys.argv[2] # A text file containing text in the target language
target_file = sys.argv[3] # A file in which the part-of-speech pickle will be stored

nlp = spacy.load(nlp_model)

def add_sent_to_dict(sent, d):
    doc = nlp(sent)
    for token in doc:
        word = str(oken.text.lower())
        pos = str(token.pos_)
        if word not in d:
            d[word] = {}
        if pos not in d[word]:
            d[word][pos] = 0
        d[word][pos] += 1

def pickle_object(obj, filename):
    f = open(filename, "wb")

    pickle.dump(obj, f)

    f.close()

def retrieve_pickle(filename):
    f = open(filename, "rb")

    d = pickle.load(f)

    return d



try:
    d = retrieve_pickle(target_pickle)
except IOError:
    d = {}
    d["Lines"] = 0

wik = open(source_pickle)
i = 0
for line in wik:
    if len(line.strip()) > 0:
        i += 1
        if i > d["Lines"]:
            doc = nlp(line)
            for token in doc:
                word = str(token.text.lower())
                pos = str(token.pos_)
                if word not in d:
                    d[word] = {}
                if pos not in d[word]:
                    d[word][pos] = 0
                d[word][pos] += 1

            if i % 10000 == 0:
                print(i)
                d["Lines"] = i
                pickle_object(d, target_pickle)

pickle_object(d, target_pickle)

