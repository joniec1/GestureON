import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import joblib

# ====== Wczytanie danych ======

labels = ["open_hand", "fist", "thumb_up"]

X = []
y = []

for idx, label in enumerate(labels):
    data = pd.read_csv(f"data/{label}.csv", header=None)
    X.append(data.values)
    y.append(np.full(len(data), idx))

X = np.vstack(X)
y = np.hstack(y)

print("Dane:", X.shape)
print("Etykiety:", y.shape)

# ====== Podział ======

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ====== Model ======

model = MLPClassifier(
    hidden_layer_sizes=(128, 64),
    max_iter=500
)

model.fit(X_train, y_train)

# ====== Ewaluacja ======

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"Accuracy: {acc:.2f}")

# ====== Zapis ======

joblib.dump(model, "model.pkl")
print("Model zapisany jako model.pkl")