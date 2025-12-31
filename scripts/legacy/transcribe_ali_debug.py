import dashscope
from dashscope.audio.asr import Transcription
import os
import sys

dashscope.api_key = "sk-89914a06e57d465a841b92d1ea15cdf0"

file_path = "/Users/hardentie/Downloads/vscode/庙后街 8.m4a"
file_url = f"file://{file_path}"
print(f"Using file URL: {file_url}")

print("Submitting transcription job...")
try:
    job = Transcription.async_call(
        model='paraformer-v1',
        file_urls=[file_url]
    )
    
    # Print the full job response object to debug
    print("Job Response Object:", job)

    if hasattr(job, 'task_id'):
        print(f"Job submitted. ID: {job.task_id}")
        response = Transcription.wait(task=job.task_id)
        # ... processing code ...
    else:
        print("No task_id found in response!")
        if job.status_code != 200:
            print(f"Status Code: {job.status_code}")
            print(f"Message: {job.message}")

except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
