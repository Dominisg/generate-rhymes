import pyphen
import re
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

def rhymes(dict, word, level, language):
    dic = pyphen.Pyphen(lang=language)
    word = dic.inserted(word).split('-')
    result = set()
    for w in dict:
        if len(word) > level and len(w) > level and word[-level:] == w[-level:]:
            result.add("".join(w)) 
    return result

dict = read_dictionary('pl')

print(rhymes(dict, "podlewałem", 2, "pl"))


import nltk
def rhyme(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     print(syllables)
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

print(rhyme("pipeline", 1))
print(rhyme("pipeline", 2))
print(rhyme("pipeline", 3))