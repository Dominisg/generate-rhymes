# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, abort

from rhymes import rhymes_generator, get_dictionary
  
# creating a Flask app
app = Flask(__name__)
dicts = {}

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})
  
  
@app.route('/rhymes/<language>/<int:level>/<word>', methods = ['GET'])
def disp(language, level, word):
    if language not in dicts.keys():
        abort(404)

    accurate = request.args.get('inaccurate') is None

    def generate():
        for rhyme in rhymes_generator(dicts[language], word, level, accurate, language):
            yield f"{''.join(rhyme)}\n"
    return app.response_class(generate(), mimetype='text' )
  
  
if __name__ == '__main__':

    dicts['en'] = get_dictionary('en')
    dicts['pl'] = get_dictionary('pl')

    app.run(debug = True)