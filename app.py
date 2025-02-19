from flask import Flask, jsonify
from flask_cors import CORS
from generate import sample, render
import os

app = Flask(__name__)
# Allow requests from both the development and production domains
CORS(app, origins=[
    'https://letterquared.com'
])

def load_word_list():
    # Use absolute path relative to the application directory
    word_check_path = os.path.join(os.path.dirname(__file__), "word-check.txt")
    with open(word_check_path) as f:
        return set(word.strip().lower() for word in f)

# Load words once when starting server
VALID_WORDS = load_word_list()

@app.route('/generate', methods=['GET'])
def generate_puzzle():
    try:
        # Use absolute path relative to the application directory
        words_path = os.path.join(os.path.dirname(__file__), "words.txt")
        w1, w2, side_assignments = sample(words_path, verbose=False)
        layout = render(side_assignments)
        
        return jsonify({
            'layout': layout,
            'solution': {
                'word1': w1,
                'word2': w2
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/validate/<word>', methods=['GET'])
def validate_word(word):
    return jsonify({
        'valid': word.lower() in VALID_WORDS
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 