import pyphen
import re
import pickle
import os.path
# aspell -d en dump master | aspell -l en expand > en.dict 

def read_dictionary(language):
    if language not in ["en", "pl"]:
        return []
    with open(language + ".dict") as f:
        data = re.split(" |\n", f.read())

    dic = pyphen.Pyphen(lang=language)
    dict = []
    for word in data:
        dict.append(dic.inserted(word).split('-'))
    return dict

def dump_dictionary(dict, language):
    with open(language + '.pickle', 'wb') as file:
        pickle.dump(dict, file)
        file.close()
    
def get_dictionary(language):
    if (os.path.isfile(language + '.pickle')):
        with open(language + '.pickle', 'rb') as file:
            dict = pickle.load(file)
            file.close()
    else:
        dict = read_dictionary(language)
        dump_dictionary(dict, language)

    return dict

def is_sufix_equal(a, b, level, accurate):
    similar = [('b', 'p'),
               ('d', 't'),
               ('g', 'k'),
               ('w', 'f'),
               ('z', 's'),
               ('ż', 'sz'),
               ('rz', 'sz'),
               ('dź', 'ć'),
               ('ź', 'ś'),
               ('dz', 'c'),
               ('dż', 'cz'),
               ('c', 's'),
               ('ć', 'ś')]

    if (len(a) < level and len(b) < level):
        return False

    if accurate:
        if a[-level:] == b[-level:]:
            return True
    else:
        is_equal = []
        for _ in range(level):
            is_equal.append(False)

        idx = 0
        for l_syl, r_syl in zip(a[-level:],b[-level:]):
            for sim in similar:
                l0 = l_syl.replace(sim[0], sim[1])
                l1 = l_syl.replace(sim[1], sim[0])
                if l0 == r_syl or l1 == r_syl:
                    is_equal[idx] = True
                    break
            if is_equal[idx] == False:
                return False
            idx += 1

        for i in range(level):
            is_equal[0] = is_equal[0] and is_equal[i]

        return is_equal[0]

    return False

import nltk
def rhyme_en_inaccurate(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

def rhymes(dict, word, level, accurate, language):
    if (language == 'en' and not accurate):
        return rhyme_en_inaccurate(word, level)

    dic = pyphen.Pyphen(lang=language)
    word = dic.inserted(word).split('-')
    result = set()
    for w in dict:
        if is_sufix_equal(w, word, level, accurate):
            result.add("".join(w)) 
    return result

