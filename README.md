# Call-Main

## Overview
Call-Main is an AI-powered call assistant application that integrates with Twilio for handling incoming calls and media streams. It also provides a booking system for blood, plasma, and platelets donations.

## Features
- Handles incoming calls using Twilio and FastAPI.
- Provides a WebSocket endpoint for real-time communication.
- Integrates with OpenAI for AI-driven interactions.
- Sends SMS notifications for booking confirmations.
- Supports booking for blood, plasma, and platelets donations.

## Requirements
- Python 3.8+
- The following Python packages (listed in `requirements.txt`):
  - aiohappyeyeballs
  - aiohttp
  - aiohttp-retry
  - aiosignal
  - annotated-types
  - anyio
  - async-timeout
  - attrs
  - certifi
  - charset-normalizer
  - click
  - exceptiongroup
  - fastapi
  - frozenlist
  - h11
  - idna
  - multidict
  - pydantic
  - pydantic_core
  - PyJWT
  - python-dotenv
  - requests
  - sniffio
  - starlette
  - twilio
  - typing_extensions
  - urllib3
  - uvicorn
  - websockets
  - yarl

## Setup
1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd Call-Main
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root and add your API keys:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    SMS_KEY=your_sms_api_key
    BLOOD_DONATION_API_KEY=your_blood_donation_api_key
    PLASMA_DONATION_API_KEY=your_plasma_donation_api_key
    PLATELETS_DONATION_API_KEY=your_platelets_donation_api_key
    ```

## Running the Application
1. Start the FastAPI server:
    ```sh
    uvicorn main:app --host 127.0.0.1 --port 8010
    ```

2. The server will be running at `http://127.0.0.1:8010`.

## Endpoints
- `GET /`: Returns a JSON response indicating the server is running.
- `POST /incoming-call`: Handles incoming calls and returns a TwiML response to connect to the media stream.
- `POST /book-donation`: Handles booking requests for blood, plasma, and platelets donations.
- `WebSocket /media-stream`: WebSocket endpoint for real-time communication.

## License
This project is licensed under the MIT License.
