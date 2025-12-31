import dashscope
from dashscope.audio.asr import Transcription
import os
import sys
import json
import time

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
    
    # Access task_id correctly
    if job.status_code == 200:
        task_id = job.output['task_id']
        print(f"Job submitted. ID: {task_id}")
        
        print("Waiting for completion...")
        response = Transcription.wait(task=task_id)
        
        if response.status_code == 200:
            print("Job completed.")
            # print(json.dumps(response.output, indent=2, ensure_ascii=False))
            
            transcription_text = ""
            if 'results' in response.output:
                for res in response.output['results']:
                    if 'sentences' in res:
                        for sent in res['sentences']:
                            transcription_text += sent['text']
                    elif 'text' in res:
                         transcription_text += res['text']
            # Fallback check if structure is different
            if not transcription_text and 'text' in response.output:
                 # Sometimes output is just the result if single file?
                 # Need to check structure carefully. 
                 # Let's try general traversal.
                 pass

            # If still empty, try to just dump everything text-like
            if not transcription_text:
                 # Look for 'sentences' in output directly?
                 if 'sentences' in response.output:
                      for sent in response.output['sentences']:
                           transcription_text += sent['text']
            
            if not transcription_text:
                print("Could not find text in response. Dumping output:")
                print(response.output)
            else:
                print("-" * 20)
                print(transcription_text[:500] + "...")
                
                with open("transcript.txt", "w", encoding='utf-8') as f:
                    f.write(transcription_text)
                print("Saved to transcript.txt")

        else:
            print(f"Transcription failed with code {response.status_code}")
            print(response.message)
    else:
        print(f"Submission failed with code {job.status_code}")
        print(job.message)

except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
