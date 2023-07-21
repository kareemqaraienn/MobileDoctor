import joblib
import numpy as np


def make_prediction(model_path, new_data):
     
    # Load the model
    model = joblib.load(model_path)

    # Make a prediction
    predicted_disease = model.predict(new_data)
    predicted_probabilities = model.predict_proba(new_data)
    # Output the result
    # print(f'Predicted Disease: {predicted_disease[0]}')
    max_prob_index = predicted_probabilities[0].argmax()
    # print(f'Estimated Confidence: {predicted_probabilities[0][max_prob_index] * 100}%')

    return [predicted_disease[0], predicted_probabilities[0][max_prob_index] * 100]


