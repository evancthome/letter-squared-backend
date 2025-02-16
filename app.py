from flask import Flask, jsonify
from flask_cors import CORS
from generate import sample, render

app = Flask(__name__)
# Update this with your frontend domain when you deploy it
CORS(app, origins=['https://letter-squared-psi.vercel.app/'])

def load_word_list():
    with open("word-check.txt") as f:
        return set(word.strip().lower() for word in f)

# Load words once when starting server
VALID_WORDS = load_word_list()

@app.route('/generate', methods=['GET'])
def generate_puzzle():
    try:
        w1, w2, side_assignments = sample("words.txt", verbose=False)
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
    # Update to listen on all interfaces
    app.run(host='0.0.0.0', port=8080) 