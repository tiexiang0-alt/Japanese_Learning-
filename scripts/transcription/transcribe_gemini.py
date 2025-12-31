import google.generativeai as genai
import os
import time
import sys

# Placeholder for API Key - User to provide
api_key = "AIzaSyANEpdPzKlnII7-Xzp2bJvBFJitPD1AEdY"
if not api_key:
    # Fallback to hardcoded if user edits file, or prompt input
    print("Please set GOOGLE_API_KEY environment variable or edit script.")
    sys.exit(1)

genai.configure(api_key=api_key)

file_path = "/Users/hardentie/Downloads/vscode/庙后街 8.m4a"

if not os.path.exists(file_path):
    print(f"Error: File {file_path} not found.")
    sys.exit(1)

print(f"Uploading {file_path} to Gemini...")
try:
    audio_file = genai.upload_file(file_path)
    print(f"Uploaded file: {audio_file.name}")
    
    # Wait for processing
    while audio_file.state.name == "PROCESSING":
        print('.', end='', flush=True)
        time.sleep(2)
        audio_file = genai.get_file(audio_file.name)
    
    if audio_file.state.name == "FAILED":
        print("\nFile processing failed.")
        sys.exit(1)
        
    print(f"\nFile is ready: {audio_file.state.name}")
    
    # Generate content
    print("Generating transcription with Gemini 3 Pro Preview...")
    model = genai.GenerativeModel("gemini-3-pro-preview")
    
    prompt = """
    请识别这个音频文件。
    注意：这是一场使用河南话进行的会议。
    请提供：
    1. 详细的逐字逐句的文字记录 (Transcript)。
    2. 基于内容的详细分析 (Analysis)。
    """
    
    response = model.generate_content([audio_file, prompt])
    
    output_text = response.text
    print("-" * 20)
    print(output_text[:500] + "...")
    
    with open("transcript_gemini.txt", "w", encoding='utf-8') as f:
        f.write(output_text)
    print("Saved to transcript_gemini.txt")
    
    # Clean up? 
    # genai.delete_file(audio_file.name)

except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
