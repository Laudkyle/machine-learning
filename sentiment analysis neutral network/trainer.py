import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Flatten
import tensorflow as tf
import json
# Load the synthetic dataset
with open('sentiment_dataset.json', 'r') as file:
    data = json.load(file)

# Extract features and labels
X = [item['text'] for item in data]
y = [item['label'] for item in data]

# Convert labels to numerical format
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Convert text to numerical features using CountVectorizer
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_val_vectorized = vectorizer.transform(X_val)

# Convert scipy.sparse.csr_matrix to a TensorFlow SparseTensor
X_train_sparse_tensor = tf.sparse.SparseTensor(
    indices=np.column_stack(X_train_vectorized.nonzero()),
    values=X_train_vectorized.data,
    dense_shape=X_train_vectorized.shape
)

X_val_sparse_tensor = tf.sparse.SparseTensor(
    indices=np.column_stack(X_val_vectorized.nonzero()),
    values=X_val_vectorized.data,
    dense_shape=X_val_vectorized.shape
)

# Ensure sorted indices for sparse tensors
X_train_sparse_tensor = tf.sparse.reorder(X_train_sparse_tensor)
X_val_sparse_tensor = tf.sparse.reorder(X_val_sparse_tensor)

# Build a simple neural network
model = Sequential()
model.add(Embedding(input_dim=len(vectorizer.get_feature_names_out()), output_dim=100, input_length=X_train_vectorized.shape[1]))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(3, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train_sparse_tensor, y_train, epochs=5, batch_size=32, validation_data=(X_val_sparse_tensor, y_val))

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_val_sparse_tensor, y_val)
print(f'Validation Accuracy: {test_accuracy}')

# Save the trained model and vectorizer for later use
model.save('sentiment_model_nn.h5')
joblib.dump(vectorizer, 'vectorizer_nn.joblib')
joblib.dump(label_encoder, 'label_encoder_nn.joblib')
