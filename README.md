# Vocalytics: Empowering Voices with AI
### DubHacks '24

## Goal

Our goal for this project is to leverage the power of generative AI to create a transcription service specifically designed to assist individuals with speaking disabilities. By providing accurate and real-time transcriptions, we aim to enhance communication and accessibility for those who face challenges in verbal communication.

## Overview

This project consists of two main components: the frontend and the backend. Each component plays a crucial role in capturing audio, processing it, and delivering the transcribed text.

### Frontend

The frontend captures live audio from the user's microphone, sends it to the backend for transcription, and displays the resulting text on the webpage. It provides a simple user interface with buttons to start and stop the recording and an area to display the transcribed text.

For more detailed information, refer to the [Frontend README](frontend/README.md).

### Backend

The backend is hosted on AWS Lambda and is responsible for processing the audio data received from the frontend. It converts the base64 encoded audio to `.wav` format, transcribes the audio using Amazon Transcribe, and enhances the transcription using generative AI models.

For more detailed information, refer to the [Backend README](backend/README.md).

## Roadmap

1. **Develop the frontend**: Create a user-friendly interface for capturing audio and displaying transcriptions.
2. **Implement the backend**: Set up AWS Lambda functions to handle audio processing and transcription.
3. **Integrate generative AI**: Enhance the transcriptions using advanced AI models to improve accuracy and readability.
4. **Testing and Deployment**: Ensure the system works seamlessly and deploy it for public use.

## External Resources

- **Frontend README**: Detailed documentation for the frontend can be found [here](frontend/README.md).
- **Backend README**: Detailed documentation for the backend can be found [here](backend/README.md).