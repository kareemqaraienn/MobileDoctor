import joblib
import numpy as np

# def make_prediction(model_path, new_data):
#     # Load the model
#     model = joblib.load(model_path)

#     # Make a prediction
#     predicted_probabilities = model.predict_proba(new_data)

#     # Get the indices of the top 3 probabilities
#     top_3_indices = np.argsort(predicted_probabilities[0])[-3:][::-1]

#     # Output the top 3 diseases and their probabilities
#     for i, index in enumerate(top_3_indices):
#         disease = model.classes_[index]  # Assuming your model has classes_ attribute which stores the class labels
#         probability = predicted_probabilities[0][index]
#         print(f'Predicted Disease {i+1}: {disease}, Estimated Confidence: {probability * 100}%')



# This is for printing the disease with highest probability compared to the top function that prints top 3
# import joblib
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


