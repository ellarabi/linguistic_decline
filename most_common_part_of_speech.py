
source_file = sys.argv[2] # A pickle file generated by part_of_speech.py
target_file = sys.argv[3] # A pickle file which will contain the most common part of speech for each word

f = open(source_file, "rb")

poss = pickle.load(f)

f.close()

l = []
d = {}

for word in poss:
    if word != "Lines":
        p = max(poss[word], key=poss[word].get)
        if p not in l:
            l.append(p)
            print(p)
            print(word)
            print(poss[word])
        if p == "NOUN":
            d[word] = "N"
        elif p == "VERB":
            d[word] = "V"
        elif p == "ADJ":
            d[word] = "J"
        elif p == "ADV":
            d[word] = "R"
        else:
            d[word] = "X"

f = open(target_file, "wb")

pickle.dump(d, f)

f.close()