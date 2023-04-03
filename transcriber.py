import os
import asyncio
from deepgram import Deepgram
from google.cloud import storage
from summarizer import main as summarizer_main

#your deepgram API key here
dg_client = Deepgram('your deepgram API key here')

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    with open(destination_file_name, "wb") as f:
        blob.download_to_file(f)

    print(f"File {source_blob_name} downloaded to {destination_file_name}.")

async def transcribe_audio(bucket_name, source_blob_name):
    # Download the audio file to a temporary location
    tmp_file_path = f"/tmp/{source_blob_name}"
    download_blob(bucket_name, source_blob_name, tmp_file_path)

    # Transcribe the audio using Deepgram
    with open(tmp_file_path, 'rb') as audio:
        audio_data = audio.read()

    source = {'buffer': audio_data, 'mimetype': 'audio/m4a'}
    response = await dg_client.transcription.prerecorded(source, {'punctuate': True})
    transcript = response['results']['channels'][0]['alternatives'][0]['transcript']

    print("finished transcribing, calling summarizer")

    # Delete the temporary file
    os.remove(tmp_file_path)
    
    # Save the transcript to a file
    transcript_file_path = f"/tmp/{source_blob_name}_transcript.txt"
    with open(transcript_file_path, "w") as transcript_file:
        transcript_file.write(transcript)
        
    # Extract the sender from the source_blob_name
    sender = source_blob_name.split('.')[0]
    
    # Call the summarizer script's main function with the transcript
    summary = summarizer_main(transcript_file_path, sender)
    
    return summary

def transcribe_audio_sync(bucket_name, source_blob_name):
    return asyncio.run(transcribe_audio(bucket_name, source_blob_name))

