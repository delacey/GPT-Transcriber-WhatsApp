import openai
import os
from google.cloud import storage

#your openAI key here
openai.api_key = "your openAI API key here"

def read_text_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

def chunk_text(text, chunk_size):
    words = text.split()
    chunks = []

    current_chunk = []
    current_chunk_size = 0

    for word in words:
        word_size = len(word) + 1  # Adding 1 for the space character
        if current_chunk_size + word_size > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_chunk_size = 0

        current_chunk.append(word)
        current_chunk_size += word_size

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def summarize_text(text):
    token_limit = 8000
    chunk_size = token_limit * 3.5  # Adjust the chunk size as needed

    # Break the text into smaller chunks
    text_chunks = chunk_text(text, chunk_size)

    summaries = []
    for chunk in text_chunks:
        prompt = f"Summarize the following text in a way that is both comprehensive and detailed, expanding on the main points and essential details. Use a longer format for this summary:\n{chunk}\n"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        print(response)
        summary = response['choices'][0]['message']['content']
        summaries.append(summary)
        print(summaries)

    # Combine the summaries of all chunks into a single summary
    full_summary = ' '.join(summaries)
    return full_summary

def uploadsumtobucket(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with open(source_file_name, "rb") as f:
        blob.upload_from_file(f)
        
def main(input_file, sender):
    
    # Read the content of the text document
    text = read_text_file(input_file)
    
    # Summarize the text using OpenAI API
    summary = summarize_text(text)
    
    # Print the summary
    print("Summary:")
    print(summary)

    # Save the summary to a temporary file
    summary_file_path = f"/tmp/{sender}_summary.txt"
    with open(summary_file_path, "w") as summary_file:
        summary_file.write(summary)

    # Uploads to cloud
    bucket_name = "your bucket name here" #put your google cloud bucket name here
    destination_blob_name = f"{sender}_summary.txt"
    uploadsumtobucket(bucket_name, summary_file_path, destination_blob_name)

    return summary
    
if __name__ == "__main__":
    main()
