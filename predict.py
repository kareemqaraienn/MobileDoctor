'''Module for making predictions with a machine learning model.'''
import joblib

def make_prediction(model_path, new_data):
    """
    Predict the outcome using the model at model_path on new_data.
    
    Parameters:
    model_path (str): Path to the joblib file with the model.
    new_data (DataFrame/Array-like): Data for prediction.
    
    Returns:
    list: Predicted outcome and its confidence level.
    """
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
