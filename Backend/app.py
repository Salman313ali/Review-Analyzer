from flask import Flask, request, jsonify
from model_utils import analyze_review, load_model_and_tokenizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model, tokenizer = load_model_and_tokenizer('lstm_model.keras', 'tokenizer.pickle')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    review = data.get('review')
    sentiment, department,stars = analyze_review(review, model, tokenizer)
    return jsonify({'sentiment': sentiment, 'department': department, 'stars': stars})

if __name__ == '__main__':
    app.run(debug=True)
