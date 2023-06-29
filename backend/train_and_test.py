import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
import joblib

def train_and_test(cleaned_data_path, model_path):
    symptoms_and_disease = pd.read_csv(cleaned_data_path)
    
    train, test = train_test_split(symptoms_and_disease,test_size=0.2)
    X_train = train.drop("Disease",axis=1)
    y_train = train["Disease"].copy()
    X_test = test.drop("Disease",axis=1)
    y_test = test["Disease"].copy()
    
    
    rnd_forest = RandomForestClassifier()
    rnd_forest.fit(X_train,y_train)
    
    
    cross_val_score(rnd_forest,X_train,y_train,cv=10).mean()
    
    y_pred = rnd_forest.predict(X_test)
    accuracy_score(y_test,y_pred)

    X_full = symptoms_and_disease.drop("Disease", axis=1)
    y_full = symptoms_and_disease["Disease"].copy()
    rnd_forest.fit(X_full, y_full)
    joblib.dump(rnd_forest, model_path)

