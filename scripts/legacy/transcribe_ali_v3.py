import dashscope
from dashscope.audio.asr import Transcription
import os
import sys

dashscope.api_key = "sk-89914a06e57d465a841b92d1ea15cdf0"

file_path = "/Users/hardentie/Downloads/vscode/庙后街 8.m4a"

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

# Construct file URL
file_url = f"file://{file_path}"
print(f"Using file URL: {file_url}")

print("Submitting transcription job...")
try:
    job = Transcription.async_call(
        model='paraformer-v1',
        file_urls=[file_url]
    )

    print(f"Job submitted. ID: {job.task_id if hasattr(job, 'task_id') else job}")
    
    print("Waiting for completion...")
    response = Transcription.wait(task=job.task_id if hasattr(job, 'task_id') else job)
    
    if response.status_code == 200:
        if response.output:
            transcription_text = ""
            # Inspect structure
            print("Response output keys:", response.output[0].keys() if response.output else "None")
            for res in response.output:
                 if 'text' in res:
                     transcription_text += res['text']
                 elif 'sentences' in res:
                     for sent in res['sentences']:
                         transcription_text += sent['text']
            
            print("Transcription successful!")
            print("-" * 20)
            print(transcription_text[:500] + "...")
            
            with open("transcript.txt", "w") as f:
                f.write(transcription_text)
            print("Saved to transcript.txt")
        else:
            print("Response 200 but no output found.")
            print(response)
    else:
        print(f"Transcription failed with code {response.status_code}")
        print(response.message)

except Exception as e:
    print(f"An error occurred: {e}")
    # Print full error for debugging
    import traceback
    traceback.print_exc()
