from __future__ import print_function, absolute_import, unicode_literals

import os
from django.http import HttpResponse
import africastalking
import pickle

# Create your credentials
username = "sandbox"
api_key = "atsk_29fcd2b63f950192ac73a0d6a6f270b9391685d54905ffa4bc96a56996ea4737d2d00751"

# Initialize the SDK
africastalking.initialize(username, api_key)

# Get the SMS service
sms = africastalking.SMS


def send(message):
    # Define some options that we will use to send the SMS
    recipients = ["+256702431725", "+256775097505"]
    sender = '12692'
    # Send the SMS
    try:
        # Once this is done, that's it! We'll handle the rest
        response = sms.send(message, recipients, sender)
        print(response)
    except Exception as e:
        print(f"Houston, we have a problem {e}")


model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'disease_model.pkl'))
mlb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'mlb.pkl'))

# Load the trained model
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Load the MultiLabelBinarizer
with open(mlb_path, 'rb') as mlb_file:
    mlb = pickle.load(mlb_file)


def predict_disease(symptoms=None):
    if symptoms is None:
        symptoms = []
        return "No symptoms provided"
    else:
        encoded_symptoms = mlb.transform([symptoms])
        prediction = model.predict(encoded_symptoms)
        return prediction[0]


def generate_response(text, phone_number):
    steps = text.split('*')
    step_count = len(steps) - 1

    if step_count == 0:
        response = "CON Welcome to Self MediCaution \n"
        response += "Think before you Dose \n"
        response += "Enter symptoms What's the problem. eg Fever,Headache* \n"
    elif step_count == 1:
        symptoms = list(steps[0].split(","))
        symptoms = [symptom.strip().capitalize() for symptom in symptoms]
        response = "CON " + f"You are likely to be suffering from {predict_disease(symptoms)} \n"
        response += "We recommend you talk to a doctor for further diagnosis \n"
        response += "1. Contact Nearby doctor / Facility \n"
    elif step_count == 2:
        response = "CON Enter your location \n"
        response += "To find nearby doctor / Facility \n"
        response += "1. Enter your location \n"

    elif step_count == 3:
        location = steps[3]
        response = "CON " + f"doctors/ facilities around {location}  \n"
        response += "choose by entering their ids \n"
        response += "1. Dr. Morgan \n"
        response += "2. Dr Alex \n"
        response += "3. Dr Maximo"

    elif step_count == 4:
        choice = steps[4]
        if choice == "1":
            doctor = "Dr. Morgan"
            contact = "070336373878"
            email = "drmorgan@gmail.com"
            facility = "Norvik"
        elif choice == "2":
            doctor = "Dr Alex"
            contact = "077777777777"
            email = "dralex@gmail.com"
            facility = "Mengo"
        elif choice == "3":
            doctor = "Dr Maximo"
            contact = "088888888888"
            email = "drmaximo@gmail.com"
            facility = "Mulago"
        else:
            doctor = "Invalid Choice"
            contact = "N/A"
            email = "N/A"
            facility = "N/A"

        response = f"CON {doctor}, {facility} \n"
        response += f"1. call  {contact} \n"
        response += f"2. contact on Whatsapp.\n"
        response += f"3. email: {email} \n"
    elif step_count == 5:
        send(f"Patient on number {phone_number} needs your services")
        response = "END Doctor has been notified. please follow up "
    else:
        response = "END Invalid Selection"
    return response


def ussd(request):
    session_id = request.POST.get("sessionId")
    serviceCode = request.POST.get("serviceCode")
    phone_number = request.POST.get("phoneNumber")
    if request.method == "POST":
        text = request.POST.get("text", "")
    else:
        text = request.GET.get("text", "")
    response = generate_response(text, phone_number)
    print("********************************")
    print("method: ", request.method)
    print("post: ", request.POST)
    print("get: ", request.GET)
    print("text: ", text)
    print("phone: ", phone_number)
    print("session_id: ", session_id)
    print("serviceCode: ", serviceCode)
    print("********************************")

    # Send the response back to the API
    return HttpResponse(response)
