from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import re
from collections import Counter
import pickle

# Load trained model
model = tf.keras.models.load_model("url_classifier_model.h5")

# Load vocabulary
with open("vocab.pkl", "rb") as f:
    vocab = pickle.load(f)

# Function to preprocess URL
def preprocess_url(url):
    tokens = re.split(r'\W+', url)
    tokens = [token for token in tokens if token]
    token_indices = [vocab.get(token, 0) for token in tokens]
    return np.array([token_indices])

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    processed_url = preprocess_url(url)
    prediction = model.predict(processed_url)
    predicted_class = np.argmax(prediction)
    class_labels = ['phishing', 'benign', 'defacement', 'malware']
    return jsonify({"prediction": class_labels[predicted_class]})
if __name__ == '__main__':
    app.run(debug=True)
