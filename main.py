'''
This module processes disease data, trains a model, and uses it for disease prediction based on symptoms.
'''
import json
import pandas as pd
from data_cleaning import clean_data
from train_and_test import train_and_test
from predict import make_prediction



disease_description = pd.read_csv('Datasets/disease_description.csv')
disease_precaution = pd.read_csv('Datasets/disease_precaution.csv')
symptom_severity = pd.read_csv('Datasets/symptom_severity.csv')

RAW_DATA_PATH = 'Datasets/dataset.csv'
CLEANED_DATA_PATH = 'Datasets/cleaned_dataset.csv'
MODEL_PATH = 'final_model.joblib'
COLUMN_NAMES = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic_patches', 'continuous_sneezing', 'shivering', 'chills', 'watering_from_eyes', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'vomiting', 'cough', 'chest_pain', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes', 'burning_micturition', 'spotting_urination', 'passage_of_gases', 'internal_itching', 'indigestion', 'muscle_wasting', 'patches_in_throat', 'high_fever', 'extra_marital_contacts', 'fatigue', 'weight_loss', 'restlessness', 'lethargy', 'irregular_sugar_level', 'blurred_and_distorted_vision', 'obesity', 'excessive_hunger', 'increased_appetite', 'polyuria', 'sunken_eyes', 'dehydration', 'diarrhoea', 'breathlessness', 'family_history', 'mucoid_sputum', 'headache', 'dizziness', 'loss_of_balance', 'lack_of_concentration', 'stiff_neck', 'depression', 'irritability', 'visual_disturbances', 'back_pain', 'weakness_in_limbs', 'neck_pain', 'weakness_of_one_body_side', 'altered_sensorium', 'dark_urine', 'sweating', 'muscle_pain', 'mild_fever', 'swelled_lymph_nodes', 'malaise', 'red_spots_over_body', 'joint_pain', 'pain_behind_the_eyes', 'constipation', 'toxic_look_(typhos)', 'belly_pain', 'yellow_urine', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'acute_liver_failure', 'swelling_of_stomach', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'phlegm', 'blood_in_sputum', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'loss_of_smell', 'fast_heart_rate', 'rusty_sputum', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'cramps', 'bruising', 'swollen_legs', 'swollen_blood_vessels', 'prominent_veins_on_calf', 'weight_gain', 'cold_hands_and_feets', 'mood_swings', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'abnormal_menstruation', 'muscle_weakness', 'anxiety', 'slurred_speech', 'palpitations', 'drying_and_tingling_lips', 'knee_pain', 'hip_joint_pain', 'swelling_joints', 'painful_walking', 'movement_stiffness', 'spinning_movements', 'unsteadiness', 'pus_filled_pimples', 'blackheads', 'scurring', 'bladder_discomfort', 'foul_smell_ofurine', 'continuous_feel_of_urine', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']



columns = pd.read_csv(CLEANED_DATA_PATH).columns.tolist()[:-1]  # Excludes the last element
dictionary_of_symptoms = {symptom.replace("_", " ").capitalize(): symptom for symptom in columns}


def clean_and_train_new_data():
    """Clean raw data and train model using cleaned data."""
    clean_data(RAW_DATA_PATH, CLEANED_DATA_PATH)
    train_and_test(CLEANED_DATA_PATH, MODEL_PATH)


def encode(symptoms):
    """Encode symptoms into feature vector."""
    return pd.DataFrame([{col: 1 if col in symptoms else 0 for col in COLUMN_NAMES}])



def get_disease_info(predicted_disease, symptoms):
    """Gather disease information such as description, precautions, and symptom severity."""
    description = disease_description.loc[disease_description['Disease'] == predicted_disease, 'Description'].values[0]
    precautions_row = disease_precaution.loc[disease_precaution['Disease'] == predicted_disease, ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    # remove nan from precautions
    precautions_row = precautions_row.dropna(axis=1)
    # print(precautions_row.values[0])
    precautions_str = ', '.join(precautions_row.values[0].astype(str))
    severity = {symptom: int(symptom_severity.loc[symptom_severity['Symptom'] == symptom, 'weight'].values[0]) for symptom in symptoms}
    response = {
        'disease': predicted_disease,
        'description': description,
        'precautions': precautions_str,
        'symptom_severity': severity
    }
    return json.dumps(response)


def predict_input(symptoms):
    """Predict disease based on symptoms."""
    return make_prediction(MODEL_PATH, encode(symptoms))
