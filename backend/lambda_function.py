import boto3
import json
import base64
import os
import time

# Initialize Transcribe client
transcribe = boto3.client('transcribe')

# Initialize Bedrock client
bedrock = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    try:
        # Step 1: Extract base64-encoded audio data from the JSON request body
         # Extract the body from the event
        body = json.loads(event.get("body"))
    
        # Extract the base64-encoded audio data
        pre_decode = body.get("body")  # Extract base64-encoded audio string from the "body"
    
        # Decode the audio data from base64
        audio_data_base64 = json.loads(pre_decode).get("audioData")
        audio_data = base64.b64decode(audio_data_base64)

        # Step 2: Save the audio data to a temporary file (for Transcribe to process)
        temp_audio_file = '/tmp/audio.wav'
        with open(temp_audio_file, 'wb') as f:
            f.write(audio_data)

        # Step 3: Upload the file to S3 for Transcribe
        s3 = boto3.client('s3')
        bucket_name = 'XXXXXXXXXX'  # Replace with your S3 bucket name
        s3_key = 'XXXXXXXXX'  # Path in the S3 bucket where the file will be uploaded
        s3.upload_file(temp_audio_file, bucket_name, s3_key)

        # Step 4: Start the transcription job using Amazon Transcribe
        transcription_job_name = f"TranscriptionJob_{int(time.time())}"
        transcribe.start_transcription_job(
            TranscriptionJobName=transcription_job_name,
            LanguageCode='en-US',
            Media={'MediaFileUri': f's3://{bucket_name}/{s3_key}'},  # S3 location of the file
            MediaFormat='wav',
            OutputBucketName=bucket_name  # Output transcription will be stored in this bucket
        )

        # Step 5: Poll for job completion (optional but helpful for small jobs)
        status = 'IN_PROGRESS'
        while status == 'IN_PROGRESS':
            time.sleep(0.05)  # Sleep for a few seconds before checking status again
            job = transcribe.get_transcription_job(TranscriptionJobName=transcription_job_name)
            status = job['TranscriptionJob']['TranscriptionJobStatus']
            if status == 'FAILED':
                raise Exception(f"Transcription job failed: {job['TranscriptionJob']['FailureReason']}")
            if status == 'COMPLETED':
                transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
                print(f"Transcription completed. Transcript URL: {transcript_uri}")

                # Step 6: (Optional) Use Bedrock to enhance the transcription text
                enhanced_text = enhance_with_bedrock(transcript_uri)
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': f'Transcription job {transcription_job_name} completed successfully.',
                        'transcript_uri': transcript_uri,
                        'enhanced_text': enhanced_text
                    })
                }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Function to enhance the transcription with Amazon Bedrock
def enhance_with_bedrock(transcript_uri):
    try:
        # Download transcription result
        response = requests.get(transcript_uri)
        text = response.json().get('results', {}).get('transcripts', [{}])[0].get('transcript', '')

        # Use Amazon Bedrock to enhance the transcription text
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',  # Replace with the actual Bedrock model ID
            contentType='text/plain',
            accept='application/json',
            body=json.dumps({"text": text})
        )

        # Parse the response from Bedrock
        enhanced_text = json.loads(response['body'])['enhanced_text']
        return enhanced_text

    except Exception as e:
        return f"Error enhancing text: {str(e)}"
