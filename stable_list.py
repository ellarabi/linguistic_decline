
# ngrams files from google books ngrams dataset
ngrams_files = ["google_books_ngrams/eng-all/english.1gram.1800s.dat",
                "google_books_ngrams/eng-all/english.1gram.1810s.dat",
                "google_books_ngrams/eng-all/english.1gram.1820s.dat",
                "google_books_ngrams/eng-all/english.1gram.1830s.dat",
                "google_books_ngrams/eng-all/english.1gram.1840s.dat",
                "google_books_ngrams/eng-all/english.1gram.1850s.dat",
                "google_books_ngrams/eng-all/english.1gram.1860s.dat",
                "google_books_ngrams/eng-all/english.1gram.1870s.dat",
                "google_books_ngrams/eng-all/english.1gram.1880s.dat",
                "google_books_ngrams/eng-all/english.1gram.1890s.dat",
                "google_books_ngrams/eng-all/english.1gram.1900s.dat",
                "google_books_ngrams/eng-all/english.1gram.1910s.dat",
                "google_books_ngrams/eng-all/english.1gram.1920s.dat",
                "google_books_ngrams/eng-all/english.1gram.1930s.dat",
                "google_books_ngrams/eng-all/english.1gram.1940s.dat",
                "google_books_ngrams/eng-all/english.1gram.1950s.dat",
                "google_books_ngrams/eng-all/english.1gram.1960s.dat",
                "google_books_ngrams/eng-all/english.1gram.1970s.dat",
                "google_books_ngrams/eng-all/english.1gram.1980s.dat",
                "google_books_ngrams/eng-all/english.1gram.1990s.dat",
                "google_books_ngrams/eng-all/english.1gram.2000s.dat"]

pickles = ["google_books_ngrams/eng-all/pickled_eng-all_1grams_1800s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1810s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1820s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1830s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1840s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1850s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1860s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1870s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1880s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1890s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1900s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1910s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1920s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1930s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1940s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1950s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1960s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1970s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1980s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_1990s.pkl",
           "google_books_ngrams/eng-all/pickled_eng-all_1grams_2000s.pkl",]

def get_total_words():
    total_list = []
    for i in range(0, 21):
        total_list.append(get_total_words_in_decade(i))

    return total_list

def get_frequencies_multiple(totals, words):
    occs = get_occurences_multiple(words)

    for word_occs in occs:
        for i in range(0, 21):
            word_occs[i] = word_occs[i] / totals[i]

    return occs

def retrieve_pickle(decade):
    f = open(pickles[decade], "rb")

    d = pickle.load(f)

    return d

def get_occurences_in_decade_multiple(words, decade):
    d = retrieve_pickle(decade)

    occurrences = []
    for word in words:
        if word in d:
            occurrences.append(d[word])
        else:
            occurrences.append(0)

    return occurrences

def get_occurences_multiple(words):
    occ_list = []
    for i in range(0, 21):
        occ_list.append(get_occurences_in_decade_multiple(words, i))

    transposed = numpy.array(occ_list).T.tolist()

    return transposed

def get_total_words_in_decade(decade):
    d = retrieve_pickle(decade)

    total = 0
    for word in d:
        total += d[word]

    return total

def words_over_cutoff(cutoff):
    ngrams_file = open(ngrams_files[0], "r")

    words = []
    for line in ngrams_file:
        tokens = line.split()
        if tokens[0].islower() and tokens[0].isalpha():
            if int(tokens[1]) > cutoff:
                words.append(tokens[0])

    return words

#TODO: above this point to shared file

def print_stable_list(pos_dict, decl):
    totals = get_total_words()

    dfs = get_frequencies_multiple(totals, decl)

    dist = [r[0] for r in dfs]

    f = open(pos_dict, "rb")

    poss = pickle.load(f)

    f.close()

    posses = []

    for d in decl:
        if d not in poss:
            posses.append("X")
        elif poss[d][0] in "NVJR":
            posses.append(poss[d][0])
        else:
            posses.append("X")

    cutoff = min(dist)

    words = words_over_cutoff(totals[0] * cutoff)

    words = [word for word in words if len(word) >= 4]

    freqs = get_frequencies_multiple(totals, words)

    quads = []

    for i in range(0, len(freqs)):
        freq = freqs[i]
        if min(freq) > 0 and max(freq) / min(freq) < 3:
            std = numpy.std(freq) / sum(freq)
            p = "X"
            if words[i] in poss and poss[words[i]][0] in "NVJR":
                p = poss[words[i]][0]
            quads.append([words[i], std, freq[0], p])

    quads.sort(key = lambda el: el[1])

    excess_chars = 0;

    for i in range(0, len(dist)):
        f = dist[i]
        w = decl[i]
        p = posses[i]
        t = []
        for quad in quads:
            if f * 0.9 <= quad[2] and quad[2] <= f * 1.1:
                if (p == "X" and quad[3] == "N") or p == quad[3]:
                    if len(w) <= len(quad[0]) + excess_chars + 1 and len(w) >= len(quad[0]) + excess_chars - 1:
                        print(quad[0])
                        t = quad
                        excess_chars += len(quad[0]) - len(w)
                        break
        if t != []:
            quads.remove(t)
        else:
            print(w)

decl_list = sys.argv[1] # list of declining words, one per line
pos_dict = sys.argv[2] # dictionary of most common part of speech, from most_common_part_of_speech.py

f = open(decl_list, "r")

decl = [line.strip() for line in f]

f.close()

print_stable_list(pos_dict, decl)