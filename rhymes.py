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

def rhymes(dict, word, level, language):
    dic = pyphen.Pyphen(lang=language)
    print(word, level, language)
    word = dic.inserted(word).split('-')
    result = set()
    for w in dict:
        if len(word) > level and len(w) > level and word[-level:] == w[-level:]:
            result.add("".join(w)) 
    return result

import nltk
def rhyme(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)
