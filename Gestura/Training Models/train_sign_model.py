import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pickle

# Load dataset
df = pd.read_csv("sign_language_data.csv")

# Split data into features (X) and labels (y)
X = df.iloc[:, 1:].values  # Hand landmarks
y = df.iloc[:, 0].values   # Labels (signs)

# Split dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train an SVM classifier
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Evaluate model accuracy
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save trained model
with open("sign_language_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved successfully as 'sign_language_model.pkl'!")
