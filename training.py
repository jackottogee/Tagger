"""
-----------------------------------------------------------------------
training.py
-----------------------------------------------------------------------
The training script for the classifier.

Trains a CountVectorizer and Multinomial Naive Bayes classifier and 
stores them as pickles for further use.

As of last run, the accuracy is 0.86 on 70% of the training data.
"""
import csv
from utils import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# processing the data 
rows = []
y = []
with open("data.csv", "r+", encoding="utf-8") as f:
    data = csv.reader(f)
    for line in data:
        for field in data:
            row = preprocessing(field[2])
            y.append(field[3])
            rows.append(row)

vectoriser = CountVectorizer(analyzer="word", ngram_range=(1,4), lowercase=False, max_features=4000)
X = vectoriser.fit_transform(rows)
with open("models/vectoriser.pkl", "wb") as v:
    pickle.dump(vectoriser, v)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=123)

mnb = MultinomialNB()
mnb.fit(X_train, y_train)
y_pred = mnb.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.02f}")

with open("models/model.pkl", "wb") as m:
    pickle.dump(mnb, m)