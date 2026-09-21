import tensorflow as tf
import numpy as np
import re
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load your trained model
model = tf.keras.models.load_model("url_classifier_model.h5")  # Ensure this is your actual model filename

# Function to preprocess URL (modify as per your training data)
def preprocess_url(url):
    url = url.lower()  # Convert to lowercase
    url = re.sub(r"https?://", "", url)  # Remove http:// or https://
    url = re.sub(r"www\.", "", url)  # Remove www.
    url = re.sub(r"[^\w\s]", "", url)  # Remove special characters
    return url
    sequence = tokenizer.texts_to_sequences([url])
    padded_sequence = pad_sequences(sequence, maxlen=10)  # Ensure maxlen matches training
    return padded_sequence

# Function to predict URL type without using vectorizer
def predict_url(url):
    processed_url = preprocess_url(url)
    prediction = model.predict(processed_url)
    return "Malicious" if prediction[0] > 0.5 else "Legitimate"


# Define Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = predict_url(url)
    return jsonify({"url": url, "prediction": result})

if __name__ == '__main__':
    app.run(debug=False)
