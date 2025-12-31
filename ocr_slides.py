import os
import subprocess
import re

# Configuration
input_dir = "extracted_slides"
output_file = "lesson_02_extracted_text_ocr.md"
langs = "jpn+chi_sim+eng" # Japanese, Chinese Simplified, English

files = sorted([f for f in os.listdir(input_dir) if f.endswith(".jpg")])

print(f"Found {len(files)} slides. Starting OCR...")

with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write("# Extracted Text from Lesson 2 Slides (OCR)\n\n")
    
    for filename in files:
        filepath = os.path.join(input_dir, filename)
        slide_num = filename.replace("slide_", "").replace(".jpg", "")
        
        print(f"Processing Slide {slide_num}...")
        
        try:
            # Run tesseract command
            # tesseract <input> stdout -l <langs>
            result = subprocess.run(
                ["tesseract", filepath, "stdout", "-l", langs],
                capture_output=True,
                text=True,
                check=True
            )
            
            text = result.stdout.strip()
            
            # Basic cleanup: remove empty lines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            cleaned_text = '\n'.join(lines)
            
            outfile.write(f"## Slide {slide_num}\n")
            if cleaned_text:
                outfile.write(cleaned_text + "\n")
            else:
                outfile.write("(No text detected)\n")
            outfile.write("\n")
            
        except subprocess.CalledProcessError as e:
            print(f"Error processing {filename}: {e}")
            outfile.write(f"## Slide {slide_num}\n(Error during OCR)\n\n")

print("Done! Check", output_file)
