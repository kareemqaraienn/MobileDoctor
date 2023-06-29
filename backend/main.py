import os

# Change the current directory to 'src'
os.chdir('backend')

# Get the current working directory
current_directory = os.getcwd()

# List all files and directories in the current directory
files_and_directories = os.listdir(current_directory)

# Print the list of files and directories
print("Current Directory:", current_directory)
print("Files and Directories:")
for item in files_and_directories:
    print(item)


from data_cleaning import clean_data
from train_and_test import train_and_test
from predict import make_prediction

# Define paths
raw_data_path = '../Datasets/dataset.csv'
cleaned_data_path = '../Datasets/cleaned_dataset.csv'
model_path = 'final_model.joblib'

# # Clean the data
# clean_data(raw_data_path, cleaned_data_path)

# # Train and test the model
# train_and_test(cleaned_data_path, model_path)
def clean_and_train_new_data():
    clean_data(raw_data_path, cleaned_data_path)
    train_and_test(cleaned_data_path, model_path)
print('done')





# # Extract column names and exclude the last column 'Disease'
# column_names = [col for col in cleaned_df.columns if col != 'Disease']



# # Make a prediction
# input_features = encode(symptoms)
# prediction = make_prediction(model_path, input_features)

# def encode(symptoms):
#     header = pd.read_excel(cleaned_data_path, nrows=0)

#     # Extract column names and exclude the last column 'Disease'
#     column_names = [col for col in header.columns if col != 'Disease']
    
#     return pd.DataFrame([{col: 1 if col in symptoms else 0 for col in column_names}])

import pandas as pd

def encode(symptoms):
    header = pd.read_csv(cleaned_data_path, nrows=0)

    # Extract column names and exclude the last column 'Disease'
    column_names = [col for col in header.columns if col != 'Disease']
    
    return pd.DataFrame([{col: 1 if col in symptoms else 0 for col in column_names}])

# Extract column names and exclude the last column 'Disease'
# Read only the header row (column names) of the Excel file
header = pd.read_csv(cleaned_data_path, nrows=0)

# Extract column names and exclude the last column 'Disease'
column_names = [col for col in header.columns if col != 'Disease']

# new_symptoms =  [ 'chills', 'fatigue', 'cough', 'high_fever' ,'breathlessness' ,'malaise' , 'phlegm','chest_pain', 'fast_heart_rate' ,'rusty_sputum']
new_symptoms = ['itching' ,'skin_rash', 'stomach_pain' ,'spotting_urination']


def predict_input(symptoms):
    make_prediction(model_path, encode(symptoms))

predict_input(new_symptoms)

# Make a prediction
# input_features = encode(new_symptoms)
# prediction = make_prediction(model_path, input_features)



    