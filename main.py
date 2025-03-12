import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from dotenv import load_dotenv
import requests
from openai import OpenAI

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SMS_KEY = os.getenv('SMS_KEY')
PORT = int(os.getenv('PORT', 8010))
from datetime import datetime
current_datetime = datetime.now()
current_date = current_datetime.strftime("%d-%m-%Y")
current_time = current_datetime.strftime("%I:%M %p")
SYSTEM_MESSAGE = """
Welcome to the Blood Donation Booking System. Please select an option:
1. Blood Donation
2. Plasma Donation
3. Platelets Donation
"""
VOICE = 'alloy'
LOG_EVENT_TYPES = [
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created'
]
SHOW_TIMING_MATH = False

app = FastAPI()

if not OPENAI_API_KEY:
    raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running 555!"}

@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response to connect to Media Stream."""
    body = await request.body()
    print("Headers:", request.headers)
    print("Body:", body.decode())
    response = VoiceResponse()
    # <Say> punctuation to improve text-to-speech flow
    response.say("Hello there! I am an AI call assistant created by Aman Patel")
    response.pause(length=1)
    response.say("O.K. you can start talking!")
    host = "api.amanpatel.in" #request.url.hostname
    connect = Connect()
    connect.stream(url=f'wss://{host}/media-stream')
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")

@app.websocket("/media-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(SYSTEM_MESSAGE)
    while True:
        data = await websocket.receive_text()
        if data == "1":
            await websocket.send_text("You selected Blood Donation. Please provide your details.")
            # Handle blood donation booking
        elif data == "2":
            await websocket.send_text("You selected Plasma Donation. Please provide your details.")
            # Handle plasma donation booking
        elif data == "3":
            await websocket.send_text("You selected Platelets Donation. Please provide your details.")
            # Handle platelets donation booking
        else:
            await websocket.send_text("Invalid option. Please select a valid option.")

async def send_initial_conversation_item(openai_ws):
    """Send initial conversation item if AI talks first."""
    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Hello there! I am an AI call assistant created by Aman Patel. How can I help you?'"
                }
            ]
        }
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))


async def initialize_session(openai_ws):
    """Control initial session with OpenAI."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))

    # Uncomment the next line to have the AI speak first
    # await send_initial_conversation_item(openai_ws)
    
async def send_sms():
    url = "https://www.fast2sms.com/dev/bulkV2"
    api_key = SMS_KEY
    msg='Your test booking is confirmed! Details: \nPhone: 9462255025 \nCity: Bangalore \nTest: Blood Test \nDate: 06-12-2024 \nTime: 10:00AM \nCollection: In-Clinic Collection  \nThank you for choosing us!'
    querystring = {
        "authorization": api_key,
        "message": msg,
        "language": "english",
        "route": "q",
        "numbers": "9462255025"
    }
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json() 

@app.post("/book-donation")
async def book_donation(request: Request):
    data = await request.json()
    option = data.get("option")
    if option == "1":
        return await book_blood_donation(data)
    elif option == "2":
        return await book_plasma_donation(data)
    elif option == "3":
        return await book_platelets_donation(data)
    else:
        return JSONResponse(status_code=400, content={"message": "Invalid option"})

async def book_blood_donation(data):
    # Implement blood donation booking logic here
    return {"message": "Blood donation booking successful"}

async def book_plasma_donation(data):
    # Implement plasma donation booking logic here
    return {"message": "Plasma donation booking successful"}

async def book_platelets_donation(data):
    # Implement platelets donation booking logic here
    return {"message": "Platelets donation booking successful"}

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Create a completion request
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
)

# Print the completion result
print(completion.choices[0].message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
