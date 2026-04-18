# coding: utf-8

import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score

# ---------------- DATASET (IMPROVED) ----------------
data = {
    "text": [
        "I love this product", "This is amazing", "Very good experience",
        "I hate this", "Worst service ever", "Not good at all",
        "I am very happy", "This is bad", "Absolutely fantastic",
        "Terrible experience", "I like this", "So nice",
        "Awful product", "Really bad", "Excellent work",
        "Superb quality", "Horrible service", "Very disappointing"
    ],
    "label": [
        "positive","positive","positive",
        "negative","negative","negative",
        "positive","negative","positive",
        "negative","positive","positive",
        "negative","negative","positive",
        "positive","negative","negative"
    ]
}

df = pd.DataFrame(data)

# ---------------- PREPROCESS ----------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

df["clean_text"] = df["text"].apply(clean_text)

# ---------------- FEATURES ----------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["clean_text"])
y = df["label"]

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------- MODEL ----------------
model = MultinomialNB()
model.fit(X_train, y_train)

# ---------------- EVALUATION ----------------
y_pred = model.predict(X_test)

print("\nModel Performance:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred, average="weighted"))

# ---------------- PREDICT FUNCTION ----------------
def predict_sentiment(text):
    text = clean_text(text)
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# ---------------- CLI ----------------
print("\nType text to analyze sentiment (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Exiting...")
        break

    if user_input.strip() == "":
        print("Please enter some text")
        continue

    result = predict_sentiment(user_input)
    print("Sentiment:", result)