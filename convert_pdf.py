import pymupdf  # fitz
import os

pdf_path = "02课：事物代词、疑问句数字0-100_20251226003117.pdf"
output_dir = "pdf_images"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Opening {pdf_path}...")
try:
    doc = pymupdf.open(pdf_path)
    for i, page in enumerate(doc):
        print(f"Converting page {i+1}/{len(doc)}...")
        pix = page.get_pixmap(dpi=150)  # Moderate DPI for balance of quality/size
        output_file = os.path.join(output_dir, f"page_{i+1:03d}.png")
        pix.save(output_file)
    print("Conversion complete!")
except Exception as e:
    print(f"Error: {e}")
