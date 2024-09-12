import os
from django.http import HttpResponse
import africastalking
from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
def ussd(request):
    session_id = request.POST.get("sessionId")
    serviceCode = request.POST.get("serviceCode")
    phone_number = request.POST.get("phoneNumber")
    text = request.POST.get("text", "")

    print(text)

    steps = text.split('*')
    step_count = len(steps) - 1

    if step_count == 0:
        response = "CON Welcome to Self MediCaution \n"
        response += "Think before you Dose \n"
        response += "1. what's the problem. end with *1 eg fever,headache*1 \n"
    elif step_count == 1:
        response = "CON You are likely to be suffering from Malaria \n"
        response += "We recommend you talk to a doctor to get prescription \n"
        response += "1. Contact Nearby doctor / Facility \n"
    elif step_count == 2:
        response = "CON Enter your location \n"
        response += "To find nearby doctor / Facility \n"
        response += "1. Enter your location \n"
        response += "2. Skip this step"

    elif step_count == 3:
        response = "CON Near doctors \n"
        response += "1. Dr. Morgan \n"
        response += "2. Dr Alex \n"
        response += "3. Dr Maximo"

    elif step_count == 4:
        response = "CON Dr. Morgan, Mulago \n"
        response += "1. call  070336373878 \n"
        response += "2. contact on Whatsapp.\n"
        response += "3. email: drmorgan@gmail.com \n"
        response += "4. Skip this step"
    elif step_count == 5:
        send("Patient on number 08900987 needs your services")
        response = "END Doctor has been notified. please follow up "
    else:
        response = "END Invalid Selection"
    return HttpResponse(response)


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
