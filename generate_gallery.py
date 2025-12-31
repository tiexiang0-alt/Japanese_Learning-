import os

html = "<html><body>"
files = sorted([f for f in os.listdir("extracted_slides") if f.endswith(".jpg")])
for f in files:
    html += f"<div><h3>{f}</h3><img src='{f}' style='max-width: 100%; border: 1px solid black;'/></div><br/>"
html += "</body></html>"

with open("extracted_slides/gallery.html", "w") as f:
    f.write(html)
