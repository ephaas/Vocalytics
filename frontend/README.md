# Frontend Code

## Overview

This is the frontend code for the `Vocalytics` application. The frontend captures audio from the user's microphone, sends it to the backend for transcription and enhancement, and displays the transcribed text.

## Dependencies

The following dependencies are required for this frontend:

- `Google Fonts API`: Used to import custom fonts for the application. The fonts are defined in [styles.css](styles.css).

```css
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
```

## Code Structure

### HTML

The main HTML file is [index.html](index.html). It sets up the basic structure of the application, including the UI controls and the transcription display area.

### CSS

The styles for the application are defined in [styles.css](styles.css). It includes styles for buttons, the transcription box, and other UI elements.

### JavaScript

The main JavaScript logic is implemented in [app.js](app.js). It handles audio recording, sending the audio to the backend, and displaying the transcribed text.

### Example Usage

The frontend captures audio, converts it to base64, and sends it to the backend for transcription and enhancement.

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
```

### Local Development

To set up a local development environment, use the provided [local_host_setup](local_host_setup) script. This script installs `http-server` and starts a local server on port 8000.

```bash
#!/bin/bash/
npm install -g http-server
http-server -p 8000
