# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from rhymes import rhymes_generator, get_dictionary
#import nltk
#nltk.download('averaged_perceptron_tagger')
import spacy

# creating a Flask app
app = Flask(__name__)
CORS(app)
dicts = {}
nlp = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):

        data = "hello world"
        return jsonify({'data': data})


@app.route('/rhymes/<language>/<int:level>/<word>', methods=['GET'])
def disp(language, level, word):
    if language not in dicts.keys():
        abort(404)

    accurate = request.args.get('inaccurate') is None

    def generate():
        for rhyme in rhymes_generator(dicts[language], word, level, accurate,
                                      language):
            sp = nlp[language](''.join(rhyme))
            yield '{"word":"' + ''.join(rhyme) + '","partOfSpeech":"' + sp[0].pos_ + '","lemma":"' + sp[0].lemma_ + '"}\n'

    return app.response_class(generate(), mimetype="application/stream+json")


if __name__ == '__main__':

    dicts['en'] = get_dictionary('en', True)
    dicts['pl'] = get_dictionary('pl', True)
    nlp['en'] = spacy.load('en_core_web_md')
    nlp['pl'] = spacy.load('pl_core_news_md')

    app.run(debug=True)
