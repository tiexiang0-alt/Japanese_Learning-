import google.generativeai as genai
import os
import sys

# API Key - reusing the one provided
api_key = "AIzaSyANEpdPzKlnII7-Xzp2bJvBFJitPD1AEdY"
genai.configure(api_key=api_key)

transcript_file = "transcript_funasr.txt"

if not os.path.exists(transcript_file):
    print(f"Error: {transcript_file} not found.")
    sys.exit(1)

print("Reading transcript...")
with open(transcript_file, "r", encoding='utf-8') as f:
    transcript_text = f.read()

print(f"Transcript length: {len(transcript_text)} characters")

print("Generating analysis with Gemini 3 Pro Preview...")
try:
    model = genai.GenerativeModel("gemini-3-pro-preview")
    
    prompt = f"""
    以下是一场使用河南话进行的会议的逐字记录。
    请对该内容进行详细分析。
    
    请提供：
    1. 会议概要 (Executive Summary)
    2. 主要议题 (Key Topics)
    3. 详细内容分析 (Detailed Analysis)
    4. 待办事项或结论 (Action Items / Conclusions)
    5. 任何值得注意的方言表达或文化背景 (Dialect/Cultural Notes)

    Transcript:
    {transcript_text}
    """
    
    response = model.generate_content(prompt)
    
    output_text = response.text
    print("-" * 20)
    print(output_text[:500] + "...")
    
    with open("analysis_gemini.md", "w", encoding='utf-8') as f:
        f.write(output_text)
    print("Saved to analysis_gemini.md")

except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
