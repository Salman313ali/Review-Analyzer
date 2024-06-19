from flask import Flask, request, jsonify
import joblib
from model_utils import analyze_review
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

joblib.load('model.pkl') 

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    review = data.get('review')
    sentiment, department = analyze_review(review, model)

    return jsonify({'sentiment': sentiment, 'department': department})

if __name__ == '__main__':
    app.run(debug=True)
