# Blood Donation Booking System

This is a FastAPI application for handling blood donation bookings via phone calls using Twilio.

## Features

- Handles incoming calls and plays an automated menu.
- Allows users to choose between blood, plasma, and platelets donation.
- Sends SMS notifications to users.
- Maintains a queue for plasma donors.

## Requirements

- Python 3.7+
- FastAPI
- Twilio
- python-dotenv
- pyngrok
- uvicorn

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Install the required dependencies:
    ```sh
    pip install fastapi twilio python-dotenv uvicorn pyngrok
    ```

3. Create a [.env](http://_vscodecontentref_/0) file in the root directory and add your Twilio credentials:
    ```
    TWILIO_ACCOUNT_SID=your_account_sid
    TWILIO_AUTH_TOKEN=your_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_phone_number
    ```

## Running the Application

1. Start the FastAPI application:
    ```sh
    uvicorn main:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`.

## Endpoints

- `GET /incoming-call`: Handles incoming calls and plays the automated menu.
- `POST /handle-response`: Handles the user's keypad input (DTMF tones).
- `GET /queue-status`: Check the Plasma donor queue.

## License

This project is licensed under the MIT License.
