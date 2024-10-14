# Backend Code

## Overview

This is the Python code for the `TranscribeFunction` hosted on AWS Lambda. The program functions as follows:

1. Receive a JSON event containing base64 encoded audio through an HTTP API created via AWS API Gateway.
2. Convert the base64 encoded audio to `.wav` format.
3. Transcribe the audio file using Amazon Transcribe.
4. Correct grammar and enhance the text utilizing the Claude 3.5 Generative AI model through Amazon Bedrock.
5. Send a JSON containing the generative AI enhanced text back to the client through API Gateway.

## Dependencies

The following dependencies are required for this function:

- `boto3`: AWS SDK for Python to interact with AWS services.
- `json`: To parse JSON data.
- `base64`: To decode base64 encoded audio.
- `os`: To handle file operations.
- `time`: To manage time-related operations.

## Code Structure

The main logic is implemented in the [`lambda_handler`](backend/lambda_function.py) function in [backend/lambda_function.py](backend/lambda_function.py). The transcription enhancement is handled by the [`enhance_with_bedrock`](backend/lambda_function.py) function.

### Example Usage

The frontend code in [frontend/app.js](frontend/app.js) captures audio, converts it to base64, and sends it to the backend for transcription and enhancement.

```js
document.getElementById('start').addEventListener('click', function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            const audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    const base64AudioMessage = reader.result.split(',')[1];
                    
                    fetch('https://XXXXXX.execute-api.us-west-2.amazonaws.com/TranscribeFunction', {
                        method: 'POST',
                        headers: { 
                            'Content-Type': 'application/json', 
                        },
                        body: JSON.stringify({ message: base64AudioMessage })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data && data.transcript) {
                            document.getElementById('textOutput').textContent = data.transcript;
                        } else {
                            document.getElementById('textOutput').textContent = "No transcription available";
                        }
                    })
                    .catch(error => {
                        console.error("Error in fetch request:", error);
                        document.getElementById('textOutput').textContent = "Failed to get transcription";
                    });
                };
            });

            document.getElementById('stop').disabled = false;
            document.getElementById('stop').addEventListener('click', () => {
                mediaRecorder.stop();
                document.getElementById('stop').disabled = true;
            });
        });
});
