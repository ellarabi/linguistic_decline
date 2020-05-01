

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

def dict_from_file(decade):
    ngrams_file = open(ngrams_files[decade], "r")

    occ_dict = {}

    for line in ngrams_file:
        tokens = line.split()
        word = tokens[0].lower()
        if word not in occ_dict:
            occ_dict[word] = int(tokens[1])
        else:
            occ_dict[word] += int(tokens[1])

    return occ_dict

def pickle_object(obj, decade):
    f = open(pickles[decade], "wb")

    pickle.dump(obj, f)

    f.close()

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

def get_frequencies_multiple(totals, words):
    occs = get_occurences_multiple(words)

    for word_occs in occs:
        for i in range(0, 21):
            word_occs[i] = word_occs[i] / totals[i]

    return occs

def get_total_words():
    total_list = []
    for i in range(0, 21):
        total_list.append(get_total_words_in_decade(i))

    return total_list

def words_over_cutoff(cutoff):
    ngrams_file = open(ngrams_files[0], "r")

    words = []
    for line in ngrams_file:
        tokens = line.split()
        if tokens[0].islower() and tokens[0].isalpha():
            if int(tokens[1]) > cutoff:
                words.append(tokens[0])

    return words

def decline_metric_3(freq, decline_factor, min_decade):
        total = sum(freq)

        freq = [f / total for f in freq]

        best_fit = 100
        best_dec = -1
        best_curve = []

        if max(freq) < decline_factor * freq[20]:
            return 100

        for zero_dec in range(2, 21):
            line = [zero_dec - i - 1 for i in range(0, zero_dec)]

            arr_freq = numpy.array(freq[0:zero_dec])
            arr_line = numpy.array(line)

            lin, a, b, c = scipy.linalg.lstsq(arr_line[:, numpy.newaxis], arr_freq)
            curve = [max((zero_dec - i - 1) * lin[0], 0) for i in range(0, 21)]

            arr_fit = numpy.array(curve)
            fit = numpy.linalg.norm(arr_fit - numpy.array(freq))

            if fit < best_fit:
                best_curve = curve
                best_fit = fit
                best_dec = zero_dec

        if best_dec < min_decade:
            return 100

        return best_fit

def print_declining_list(n, cutoff_f, decline_factor, min_decade, min_length):
    totals = get_total_words()

    words = words_over_cutoff(totals[0] * cutoff_f)

    words = [word for word in words if len(word) >= min_length]

    freqs = get_frequencies_multiple(totals, words)

    metrics = []

    for i in range(0, len(freqs)):
        freq = freqs[i]
        deviance = decline_metric_3(freq, decline_factor, min_decade)
        metrics.append([words[i], deviance])

    metrics.sort(key = lambda el: el[1])


    for pair in metrics[0:n]:
        if pair[1] < 50:
            print(pair[0])

n = sys.argv[1] # maximum number of words to print
cutoff_f = sys.argv[2] # minimum initial frequency for declining word (we used 0.000005)
decline_factor = sys.argv[3] # times by which word had to decline to be included (we used 10)
min_decade = sys.argv[4] # decade which line of best fit must reach 0 by (we used 10)
min_length = sys.argv[5] # minimum length of declining words in character (we used 4)

for i in range (0, 21):
    try:
        retrieve_pickle(i)
    except IOError:
        d = dict_from_file(i)
        pickle_object(d, i)


print_declining_list(n, cutoff_f, decline_factor, min_decade, min_length)