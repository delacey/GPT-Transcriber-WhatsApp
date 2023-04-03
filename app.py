import os
import requests
import tempfile
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from google.cloud import storage
from transcriber import transcribe_audio_sync

# Replace with your Twilio account SID and auth token
TWILIO_ACCOUNT_SID = 'your SID here'
TWILIO_AUTH_TOKEN = 'your auth token here'

if 'GOOGLE_APPLICATION_CREDENTIALS_CONTENT' in os.environ:
    temp_credentials_file, temp_credentials_path = tempfile.mkstemp()
    with open(temp_credentials_file, 'w') as f:
        f.write(os.environ['GOOGLE_APPLICATION_CREDENTIALS_CONTENT'])
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_credentials_path

app = Flask(__name__)

def download_m4a_file(media_url, file_path):
    response = requests.get(media_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

def handle_incoming_attachment(request):
    media_url = request.form.get('MediaUrl0')
    media_type = request.form.get('MediaContentType0')
    sender = request.form.get('From')

    if media_type == 'audio/mp4':
        # Download the M4A file
        file_path = f"{sender}.m4a"
        download_m4a_file(media_url, file_path)
        bucket_name = "your bucket name here" #put your google cloud storage bucket name here
        destination_blob_name = f"{sender}.m4a"
        upload_blob(bucket_name, file_path, destination_blob_name)
        send_whatsapp_message(f"{sender}", "File received, now processing. Don't send another file until you receive the summary from this one.")

        
        # Get the summary from the transcribe_audio function
        summary = transcribe_audio_sync(bucket_name, destination_blob_name)

        # Send the summary back to the sender as a WhatsApp message
        print(f"Sending summary back to: {sender}")
        send_whatsapp_message(f"{sender}", f"Summary: {summary}")
        
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with open(source_file_name, "rb") as f:
        blob.upload_from_file(f)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    
@app.route('/whatsapp/', methods=['POST'])
def handle_whatsapp_message():
    print("Received a request")
    handle_incoming_attachment(request)
    print("Finished handling attachment")

    # Add this block of code to create and return a TwiML response
    twiml_response = MessagingResponse()
    return str(twiml_response)

def send_whatsapp_message(to, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Split the message body into smaller parts if it exceeds 1600 characters
    message_parts = [body[i:i + 1550] for i in range(0, len(body), 1550)]

    for part in message_parts:
        message = client.messages.create(
            body=part,
            from_='whatsapp:+14151111111',  # Replace with your Twilio phone number 
            to=to
        )
        
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)))
