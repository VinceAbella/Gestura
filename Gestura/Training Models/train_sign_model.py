import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pickle

df = pd.read_csv("sign_language_data.csv")

X = df.iloc[:, 1:].values  
y = df.iloc[:, 0].values   

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = SVC(kernel='linear')
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

with open("sign_language_model.pkl", "wb") as f:
    pickle.dump(model, f)
