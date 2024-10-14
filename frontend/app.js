document.getElementById('start').addEventListener('click', function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            const audioChunks = [];  // Store all the audio chunks

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);  // Push each chunk into the array
            });

            // When the recording stops, process the entire audio file
            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' }); // Create one large audio Blob from the chunks
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);  // Convert the audio Blob to Base64
                reader.onloadend = () => {
                    const base64AudioMessage = reader.result.split(',')[1];
                    
                    // Send the entire audio blob for transcription (API URL is hidden to avoid massive AWS bill)
                    fetch('https://XXXXXX.execute-api.us-west-2.amazonaws.com/TranscribeFunction', {
                        method: 'POST',
                        headers: { 
                            'Content-Type': 'application/json', 
                        },
                        body: JSON.stringify({ message: base64AudioMessage })  // Send the Base64 audio
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Display the transcription result
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

            // Enable the stop button when recording starts
            document.getElementById('stop').disabled = false;
            document.getElementById('stop').addEventListener('click', () => {
                mediaRecorder.stop();  // Stop the recording when the stop button is clicked
                document.getElementById('stop').disabled = true;  // Disable the stop button again
            });
        });
});