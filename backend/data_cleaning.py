import pandas as pd
import warnings
warnings.simplefilter("ignore")

def clean_data(data_path, cleaned_data_path):
    # Read the data
    df = pd.read_csv(data_path)

    
    ##make sure theres no whitespace anywhere
    for i in df.columns[1:]:
        df[i] = df[i].str.strip().str.replace(" ", "")


    ## create an array of symptoms for each disease
    df["Symptoms"] = 0
    records = df.shape[0]
    for i in range(records):
        values = df.iloc[i].values
        values = values.tolist()
        if 0 in values:
            df["Symptoms"][i] = values[1:values.index(0)]
        else:
            df["Symptoms"][i] = values[1:]


    ## gather all the possible symptom values
    columns = df[['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4',
           'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9',
           'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14',
           'Symptom_15', 'Symptom_16', 'Symptom_17']].values.ravel()

    ## remove duplicates and empoty values
    unique_symptoms = pd.unique(columns)
    unique_symptoms = unique_symptoms.tolist()
    unique_symptoms = [i for i in unique_symptoms if str(i) != "nan"]

    ## make the symptoms a new df
    symptoms = pd.DataFrame(columns = unique_symptoms, index = df.index)


    symptoms["Symptoms"] = df["Symptoms"]


    for i in unique_symptoms:
        symptoms[i] = symptoms.apply(lambda x:1 if i in x.Symptoms else 0, axis=1)


    symptoms["Disease"] = df["Disease"]
    symptoms = symptoms.drop("Symptoms",axis=1)


    return symptoms.to_csv(cleaned_data_path, index=False)
