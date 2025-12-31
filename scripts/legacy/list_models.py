import google.generativeai as genai
import os

api_key = "AIzaSyANEpdPzKlnII7-Xzp2bJvBFJitPD1AEdY"
genai.configure(api_key=api_key)

print("Listing models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
