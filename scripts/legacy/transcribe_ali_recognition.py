import dashscope
from dashscope.audio.asr import Recognition
import os
import sys

dashscope.api_key = "sk-89914a06e57d465a841b92d1ea15cdf0"

file_path = "/Users/hardentie/Downloads/vscode/庙后街 8.m4a"

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

print(f"Transcribing {file_path} using Recognition (paraformer-realtime-v1)...")

try:
    # Use Recognition.call
    # Note: format usually needs to be specified if not raw pcm/wav, 
    # but let's try 'm4a' or leave it to auto-detect if possible.
    # DashScope docs say 'format' param. 
    # Valid formats: pcm, wav, opus, speex, aac, amr. 
    # m4a is container for aac. Let's try format='aac'.
    
    # Instantiate Recognition
    recognizer = Recognition(
        model='paraformer-realtime-v1',
        format='aac',
        sample_rate=16000,
        callback=None # explicit
    )
    
    # Check if call is on instance
    # But usually call takes file path?
    # Let's try calling instance.call
    responses = recognizer.call(file_path)
    
    # Recognition.call returns a generator or result?
    # If it is synchronous but real-time, it might return a generator of partial results 
    # or a final result.
    # Actually, inspecting the user-visible doc, call usually returns a generator for Realtime? 
    # Or just one result?
    # Let's handle both.
    
    full_text = ""
    
    if hasattr(responses, '__iter__') and not isinstance(responses, (str, dict)):
        for response in responses:
            if response.status_code == 200:
                # Accumulate text?
                # Realtime results usually give partial updates.
                # We need the final one or sentence ends.
                print(f"Status: {response.status_code}, RequestId: {response.request_id}")
                if response.output:
                    print(response.output)
                    # For realtime, 'sentence' field might be present.
                    # Or 'text' might be the current hypothesis.
            else:
                print(f"Error: {response.code} - {response.message}")
    else:
        # Single response
        response = responses
        if response.status_code == 200:
             print(response.output)
             if 'text' in response.output:
                 full_text = response.output['text']
             elif 'sentence' in response.output:
                 full_text = response.output['sentence']['text']
        else:
             print(f"Error: {response.code} - {response.message}")

    # Note: Realtime transcription results are complicated to stitch if we just print them.
    # But let's see the output first.
    
except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
