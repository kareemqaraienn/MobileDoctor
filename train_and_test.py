"""Module to train and test a RandomForestClassifier on a medical dataset."""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score


def train_and_test(cleaned_data_path, model_path):
    """Trains and tests a RandomForest model, and saves the model at the given path."""

    symptoms_and_disease = pd.read_csv(cleaned_data_path)

    train, test = train_test_split(symptoms_and_disease,test_size=0.2)

    x_train = train.drop("Disease",axis=1)
    y_train = train["Disease"].copy()
    x_test = test.drop("Disease",axis=1)
    y_test = test["Disease"].copy()

    rnd_forest = RandomForestClassifier()
    rnd_forest.fit(x_train,y_train)

    cross_val_score(rnd_forest,x_train,y_train,cv=10).mean()
    y_pred = rnd_forest.predict(x_test)
    accuracy_score(y_test,y_pred)

    x_full = symptoms_and_disease.drop("Disease", axis=1)
    y_full = symptoms_and_disease["Disease"].copy()
    rnd_forest.fit(x_full, y_full)

    joblib.dump(rnd_forest, model_path)
