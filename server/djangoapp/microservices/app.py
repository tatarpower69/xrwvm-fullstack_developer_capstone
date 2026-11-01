from pathlib import Path
import os
import nltk
from flask import Flask, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.data.path.insert(0, str(Path(__file__).parent))
sia = SentimentIntensityAnalyzer()
app = Flask(__name__)

@app.get('/')
def home():
    return 'Sentiment Analyzer: use /analyze/text'

@app.get('/analyze/<path:input_txt>')
def analyze_sentiment(input_txt):
    compound = sia.polarity_scores(input_txt)['compound']
    sentiment = 'positive' if compound >= 0.05 else 'negative' if compound <= -0.05 else 'neutral'
    return jsonify(sentiment=sentiment)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5050')))
