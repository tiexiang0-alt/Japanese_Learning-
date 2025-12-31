from openai import OpenAI
import os
import sys

# Initialize client
client = OpenAI(
    api_key="sk-89914a06e57d465a841b92d1ea15cdf0",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

file_path = "/Users/hardentie/Downloads/vscode/庙后街 8.m4a"

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

print(f"Transcribing {file_path} using DashScope (paraformer-v1)...")

try:
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="paraformer-v1", 
            file=audio_file,
            prompt="这是一场使用河南话进行的会议。"
        )
    
    print("Transcription successful.")
    print("-" * 20)
    print(transcription.text)
    
    output_file = "transcript.txt"
    with open(output_file, "w") as f:
        f.write(transcription.text)
    print(f"Saved to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
