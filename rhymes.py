import pyphen
import re
import pickle
import nltk
import os.path
from wordfreq import word_frequency
from functools import cmp_to_key
import sqlite3
# aspell -d en dump master | aspell -l en expand > en.dict 

def freq_cmp(a, b, language):
    return word_frequency(b, language, wordlist='large') - word_frequency(a, language, wordlist='large')

def freq_cmp_en(a, b):
    return freq_cmp(a, b, 'en')

def freq_cmp_pl(a, b):
    return freq_cmp(a, b, 'pl')

def get_cmp(language):
    if language == 'en':
        return freq_cmp_en
    elif language == 'pl':
        return freq_cmp_pl
    return None

def read_dictionary(language):
    if language not in ["en", "pl"]:
        return []
    with open(language + ".dict") as f:
        data = re.split(" |\n", f.read())

    data = list(set(data))
    data = sorted(data, key=cmp_to_key(get_cmp(language)))

    dic = pyphen.Pyphen(lang=language)
    dict = []
    for word in data:
        dict.append(dic.inserted(word).split('-'))
    return dict

def dump_dictionary(dict, language):
    with open(language + '.pickle', 'wb') as file:
        pickle.dump(dict, file)
        file.close()

def create_db(dict, language):
    conn = sqlite3.connect(language + '.db')
    conn.execute("CREATE TABLE words (word text)")
    
    for word in dict:
        conn.execute("INSERT INTO {tn} VALUES(?)".format(tn="words"), ("-".join(word),))

    conn.commit()
    conn.close() 
    
def get_dictionary(language, sql = False):
    dict = None
    if sql:
        if not os.path.isfile(language + '.db'):
            create_db(read_dictionary(language), language)
    else:
        if (os.path.isfile(language + '.pickle')):
            with open(language + '.pickle', 'rb') as file:
                dict = pickle.load(file)
                file.close()
        else:
            dict = read_dictionary(language)
            dump_dictionary(dict, language)

    return dict

def does_sufix_rhyme(a, b, level, accurate):
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

    if a == b:
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

def rhyme_en_inaccurate(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     for (w, syllable) in syllables:
        for word, pron in entries:
            if (word == w):
                continue
            if pron[-level:] == syllable[-level:]:
                yield word

def rhymes_generator(dict, word, level, accurate, language):
    if (language == 'en' and not accurate):
        for w in rhyme_en_inaccurate(word, level):
            yield word

    dic = pyphen.Pyphen(lang=language)
    word = dic.inserted(word).split('-')
    if isinstance(dict, list):
        for w in dict:
            if does_sufix_rhyme(w, word, level, accurate):
                yield ''.join(w)
    else:
        conn = sqlite3.connect(language + '.db')
        c = conn.cursor()
        c.execute('SELECT * FROM words')
        
        for w in c:
            w = w[0].split('-')
            if does_sufix_rhyme(w, word, level, accurate):
                yield ''.join(w)
        conn.close()
            

def rhymes(dict, word, level, accurate, language):
    result = []
    for rhyme in rhymes_generator(dict, word, level, accurate, language):
        result.append(rhyme)
    return result