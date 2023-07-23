'''
Module for cleaning data related to diseases and their symptoms.
'''
import warnings

import pandas as pd

warnings.simplefilter("ignore")

def clean_data(data_path, cleaned_data_path):
    """
    Cleans the data and saves the cleaned data to a csv file.
    
    Parameters:
    data_path (str): The path to the csv file containing raw data
    cleaned_data_path (str): The path where the cleaned data will be saved
    
    Returns:
    None
    """
    # Read the data
    data_frame = pd.read_csv(data_path)

    ##make sure theres no whitespace anywhere
    for i in data_frame.columns[1:]:
        data_frame[i] = data_frame[i].str.strip().str.replace(" ", "")

    ## create an array of symptoms for each disease
    data_frame["Symptoms"] = 0
    records = data_frame.shape[0]
    for i in range(records):
        values = data_frame.iloc[i].values
        values = values.tolist()
        if 0 in values:
            data_frame["Symptoms"][i] = values[1:values.index(0)]
        else:
            data_frame["Symptoms"][i] = values[1:]


    ## gather all the possible symptom values
    columns = data_frame[['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4',
           'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9',
           'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14',
           'Symptom_15', 'Symptom_16', 'Symptom_17']].values.ravel()

    ## remove duplicates and empoty values
    unique_symptoms = pd.unique(columns)
    unique_symptoms = unique_symptoms.tolist()
    unique_symptoms = [i for i in unique_symptoms if str(i) != "nan"]

    ## make the symptoms a new data_frame
    symptoms = pd.DataFrame(columns = unique_symptoms, index = data_frame.index)

    symptoms["Symptoms"] = data_frame["Symptoms"]

    for symptom in unique_symptoms:
        symptoms[symptom] = symptoms.apply(lambda row: 1 if symptom in row.Symptoms else 0, axis=1)

    symptoms["Disease"] = data_frame["Disease"]
    symptoms = symptoms.drop("Symptoms",axis=1)


    return symptoms.to_csv(cleaned_data_path, index=False)
