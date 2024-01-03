from flask import Flask, render_template, request, jsonify
import os
import speech_recognition as sr
import joblib
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.models import load_model
import tensorflow as tf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load the vectorizer and label encoder
vectorizer = joblib.load('vectorizer_nn.joblib')
label_encoder = joblib.load('label_encoder_nn.joblib')

# Load the trained model
model = load_model('sentiment_model_nn.h5')

def predict_sentiment(text):
    # Vectorize the input text
    text_vectorized = vectorizer.transform([text])

    # Convert to TensorFlow SparseTensor
    text_sparse_tensor = tf.sparse.SparseTensor(
        indices=np.column_stack(text_vectorized.nonzero()),
        values=text_vectorized.data,
        dense_shape=text_vectorized.shape
    )

    # Ensure sorted indices for the sparse tensor
    text_sparse_tensor = tf.sparse.reorder(text_sparse_tensor)

    # Make a prediction
    prediction = model.predict(text_sparse_tensor)

    # Decode the prediction
    predicted_class = np.argmax(prediction)
    predicted_sentiment = label_encoder.classes_[predicted_class]

    return predicted_sentiment

@app.route('/')
def index():
    return render_template('index.html')

app.config['ALLOWED_EXTENSIONS'] = {'wav','m4a'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'audio' in request.files:
        # If audio file is provided
        audio_file = request.files['audio']
        if audio_file and allowed_file(audio_file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
            audio_file.save(filename)

            recognizer = sr.Recognizer()
            with sr.AudioFile(filename) as source:
                audio_data = recognizer.record(source, duration=10)
                try:
                    text = recognizer.recognize_google(audio_data)
                    sentiment = predict_sentiment(text)
                    return jsonify({'sentiment': sentiment})
                except sr.UnknownValueError:
                    return jsonify({'error': 'Could not recognize audio'})
    elif 'text' in request.form:
        # If text data is provided
        text = request.form['text']
        sentiment = predict_sentiment(text)
        return jsonify({'sentiment': sentiment})

    return jsonify({'error': 'Invalid or no data provided'})


if __name__ == '__main__':
    app.run(debug=True)
