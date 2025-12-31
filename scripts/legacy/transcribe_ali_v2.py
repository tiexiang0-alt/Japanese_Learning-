import dashscope
from dashscope.audio.asr import Transcription
from dashscope import Files
import os
import sys

dashscope.api_key = "sk-89914a06e57d465a841b92d1ea15cdf0"

file_path = "/Users/hardentie/Downloads/vscode/庙后街 8.m4a"

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

print(f"Uploading {file_path}...")
try:
    # Upload file
    # Note: trying to pass file_path directly. If api differs, we'll debug.
    # Looking at similar SDKs, upload usually takes the path.
    url = Files.upload(file_path)
    print(f"File uploaded. URL: {url}")
    
    # The return of upload might be an object or string. 
    # If it's an object, we need the url attribute. 
    # Inspecting output of Files.upload in a try-except block might be safer, 
    # but let's assume it returns a URL string or we print it to see.
    # For now, I'll assume it returns the url string directly or an object with url.
    # Actually, in some ali SDKs, it returns a URL string directly.
    # Let's verify by printing it.
    
    file_url = url
    if not isinstance(url, str):
         # If it's an object (like a dict or class), try to get URL
         if hasattr(url, 'url'):
             file_url = url.url
         elif 'url' in url:
             file_url = url['url']
         else:
             file_url = str(url) # Fallback

    print(f"Using file URL: {file_url}")

    print("Submitting transcription job...")
    job = Transcription.async_call(
        model='paraformer-v1',
        file_urls=[file_url],
        # "prompt" is not a standard parameter for async_call in dashscope typically?
        # Maybe "vocabulary" or "hotwords"? ASR typically doesn't take "prompt" like LLM.
        # However, looking at the user request "prompt"='这是一场使用河南话进行的会议', 
        # OpenAI compatible had 'prompt'.
        # For Paraformer, maybe we can't easily pass 'prompt'. 
        # But Paraformer is robust.
        # We'll skip prompt for now unless I find a param.
    )

    print(f"Job submitted. ID: {job.task_id if hasattr(job, 'task_id') else job}")
    
    print("Waiting for completion...")
    response = Transcription.wait(task=job.task_id if hasattr(job, 'task_id') else job)
    
    if response.status_code == 200:
        if response.output:
            # Depending on structure, traverse for text.
            # Usually response.output is a list of results for each file.
            transcription_text = ""
            for res in response.output:
                 if 'text' in res:
                     transcription_text += res['text']
                 elif 'sentences' in res:
                     for sent in res['sentences']:
                         transcription_text += sent['text']
            
            print("Transcription successful!")
            print("-" * 20)
            print(transcription_text[:500] + "...") # Print start
            
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
    import traceback
    traceback.print_exc()
