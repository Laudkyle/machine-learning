import joblib
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

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

# Test with input text
input_text = "I really enjoyed using this product. It exceeded my expectations!"
predicted_sentiment = predict_sentiment(input_text)
print(f"Predicted Sentiment: {predicted_sentiment}")
