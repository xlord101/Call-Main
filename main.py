import os
from fastapi import FastAPI, Request, Form, HTTPException
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
from pyngrok import ngrok

# Load API keys from .env file
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Twilio Client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# FastAPI App
app = FastAPI()

# Plasma Donor Queue (Stored in memory)
plasma_queue = []

from fastapi.responses import Response  # Import Response

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def incoming_call():
    """Handles incoming calls and plays the automated menu."""
    print("Incoming call received")  # Debugging print statement
    response = VoiceResponse()
    response.say("Welcome to the Blood Donation Booking System.")
    response.pause(length=1)
    response.say("Press 1 for Blood Donation.")
    response.say("Press 2 for Plasma Donation.")
    response.say("Press 3 for Platelets Donation.")
    response.gather(num_digits=1, action="/handle-response", method="POST")
    
    return Response(content=str(response), media_type="application/xml")  # Ensure XML response


@app.post("/handle-response")
async def handle_response(request: Request, Digits: str = Form(...)):
    """Handles the user's keypad input (DTMF tones)."""
    try:
        # Get the caller's input (digit pressed)
        form_data = await request.form()
        digits = form_data.get("Digits")
        
        # Use your verified Indian number as the recipient
        user_number = "+917499892448"  # Replace with your verified Indian number
        
        print(f"User pressed: {digits}, Caller Number: {user_number}")  # Debugging print statement

        response = VoiceResponse()

        if digits == "1":
            response.say("Thank you for choosing Blood Donation. You will receive an SMS with available slots.")
            send_sms(user_number, "Blood donation slots available: 10 AM, 2 PM, 5 PM.")
        
        elif digits == "2":
            response.say("You are added to the Plasma donation queue. Further information will be provided to you by SMS. Thank you!")
            send_sms(user_number, "Thank you! You have been added to the Plasma donation queue. You will be contacted when a donor is needed.")
            plasma_queue.append(user_number)  # Add to queue
        
        elif digits == "3":
            response.say("You are added to the Platelets donation queue. Further information will be provided to you by SMS. Thank you!")
            send_sms(user_number, "Thank you! You have been added to the Platelets donation queue. You will be contacted when a donor is needed.")
        
        else:
            response.say("Invalid input. Please call again and choose a valid option.")
        
        # End the call after playing the message
        response.hangup()
        return Response(content=str(response), media_type="application/xml")
    
    except Exception as e:
        print(f"❌ Error in handle_response: {e}")  # Debugging print statement
        raise HTTPException(status_code=500, detail="An application error occurred.")


def send_sms(to_number, message):
    """Send an SMS confirmation."""
    try:
        # Ensure the 'To' number is not the same as the 'From' number
        if to_number == TWILIO_PHONE_NUMBER:
            print(f"❌ Cannot send SMS: 'To' and 'From' numbers cannot be the same.")
            return
        
        twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"✅ SMS sent to {to_number}: {message}")  # Debugging print statement
    except Exception as e:
        print(f"❌ Failed to send SMS. Error: {e}")

@app.get("/queue-status")
async def queue_status():
    """Check the Plasma donor queue."""
    return {"Plasma Queue": plasma_queue}

# Start ngrok tunnel and display URL
try:
    public_url = ngrok.connect(8000).public_url
    print(f"🚀 Ngrok Tunnel URL: {public_url}")
except Exception as e:
    print(f"❌ Failed to start ngrok tunnel. Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)