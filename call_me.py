from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load Twilio credentials
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_INDIAN_NUMBER = "+917499892448"  # Your verified Indian number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Call the Indian number and play a message
try:
    call = client.calls.create(
        to=MY_INDIAN_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        url="https://7851-45-118-107-224.ngrok-free.app/incoming-call"  # Update this URL with your current ngrok URL
    )
    print(f"✅ Call placed successfully! Call SID: {call.sid}")
except Exception as e:
    print(f"❌ Failed to place call. Error: {e}")