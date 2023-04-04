import os
import openai
from google.cloud import storage
from summarizer import main as summarizer_main

# Set your OpenAI API key
openai.api_key = "your openai API key here"

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    with open(destination_file_name, "wb") as f:
        blob.download_to_file(f)

    print(f"File {source_blob_name} downloaded to {destination_file_name}.")

def transcribe_audio(bucket_name, source_blob_name):
    # Download the audio file to a temporary location
    tmp_file_path = f"/tmp/{source_blob_name}"
    download_blob(bucket_name, source_blob_name, tmp_file_path)

    # Transcribe the audio
    with open(tmp_file_path, 'rb') as audio_file:
        result = openai.Audio.transcribe("whisper-1", audio_file)
    transcript = result["text"]
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

