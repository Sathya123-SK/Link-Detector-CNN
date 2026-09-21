import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

# Load your trained CNN model
model = load_model("url_classifier_model.h5")  # Change to your model's path

# Load the CSV file
df = pd.read_csv("malicious_phish.csv")  # Change to your actual CSV filename

# Assuming you have already preprocessed your URLs (e.g., tokenized, embedded, or vectorized)
# You need to transform URLs into the format expected by your model.

# Example: If you used tokenization, load your tokenizer and transform URLs
# from tensorflow.keras.preprocessing.text import Tokenizer
# tokenizer = Tokenizer(num_words=10000)  # Use the same settings as in training
# X_data = tokenizer.texts_to_sequences(df['url'])
# X_data = pad_sequences(X_data, maxlen=200)  # Adjust based on your model

# Dummy transformation (replace with actual preprocessing)
X_data = np.array(df['url'].apply(lambda x: len(x)).values).reshape(-1, 1)  # Replace with your feature extraction

# Convert type labels to numeric format
label_encoder = LabelEncoder()
df['type_encoded'] = label_encoder.fit_transform(df['type'])  # Convert labels to numerical

# Predict using the CNN model
predictions = model.predict(X_data)
predicted_classes = np.argmax(predictions, axis=1)

# Identify misclassified URLs
df['predicted_type_encoded'] = predicted_classes
misclassified = df[df['type_encoded'] != df['predicted_type_encoded']]

# Save misclassified URLs to a new CSV file
misclassified[['url', 'type']].to_csv("misclassified_urls.csv", index=False)

print(f"Misclassified URLs saved to 'misclassified_urls.csv'")