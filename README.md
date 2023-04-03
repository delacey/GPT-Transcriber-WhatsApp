# GPT-Transcriber

Allows someone to send an m4a file via WhatsApp to a specified phone number via Twilio, at which point the file is transcribed by Deepgram and summarized using GPT4. The summary is then sent back to the original sender.

This project is designed to provide an efficient solution to transcribe and summarize audio from meetings, Zoom calls, or regular phone calls, and then share the summaries with team members. The project alleviates the need for manual note-taking and ensures that meeting summaries are comprehensive and accurate.

## Features

- Receive audio files through WhatsApp
- Transcribe audio using the Deepgram API
- Summarize transcriptions with OpenAI GPT-4
- Send summaries back to the sender via WhatsApp

## Limitations
- Twilio will only accept attachments of less than 16M, which is about 30 minutes worth of conversation on an Apple voice memo set to compressed. You can split longer files into multiple 30 minute chunks and send them in separately.

## Getting Started

These instructions will help you set up and deploy the project on Railway.

### Prerequisites

1. A Twilio account with a WhatsApp sandbox
2. A Railway account
3. A Google Cloud Storage account
4. A Deepgram API key
5. An OpenAI API key with GPT4 access (specify another GPT model in the summarizer.py script if you prefer)

### Deployment on Railway

1. Clone the repository:

git clone https://github.com/delacey/GPT-Transcriber.git

2. Change to the project directory:

cd GPT-Transcriber

3. Create a new Railway project:

railway init

4. Add the `GOOGLE_APPLICATION_CREDENTIALS_CONTENT` environment variable in the Railway dashboard. This should be set to the content of your Google Cloud Storage JSON key file. Make sure to replace the Twilio, Deepgram, and OpenAI API keys in the code with your own.

5. Edit the `app.py` file to replace the placeholder Twilio phone number (`'whatsapp:+14151111111'`) with your own Twilio phone number.

6. Deploy the application on Railway:

railway up

7. After deployment, Railway will provide a deployment URL.

8. Configure your Twilio WhatsApp sandbox to use the deployment URL as the webhook URL. In the Twilio dashboard, go to the "Sandbox" section under "Programmable Messaging" and set the webhook URL to the deployment URL followed by `/whatsapp/`. For example, `https://your-railway-app-url.railway.app/whatsapp/`.

9. Test the application by sending an audio file (in M4A format) to your Twilio WhatsApp sandbox number. The application will transcribe and summarize the audio, then send the summary back to you via WhatsApp.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Deepgram for providing an accurate and fast transcription service
- OpenAI GPT-4 for generating high-quality summaries
- Twilio for facilitating WhatsApp communication
- Railway for easy deployment and hosting

## Other Comments

I started out wanting to use OpenAI's whisper for the transcription piece of this project. Whisper has very good transcription quality, but I found that it would take a long time, even with their lighter models, and would often hang. Deepgram seems to be much faster and stable: you'll get your summary in one or two minutes after you send the m4a file in, while with Whisper you could be looking at ten minutes, or more, or never. I find this to be a useful timesaver and hope others do as well. 
