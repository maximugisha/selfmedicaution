import pickle

# Load the trained model
with open('./disease_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load the MultiLabelBinarizer
with open('./mlb.pkl', 'rb') as mlb_file:
    mlb = pickle.load(mlb_file)


# Example symptoms
new_symptoms = ['Chest pain', 'Fatigue', 'Loss of appetite']
new_symptoms_encoded = mlb.transform([new_symptoms])

# Predict the disease
prediction = model.predict(new_symptoms_encoded)
print(f'Predicted Disease: {prediction[0]}')
