from funasr import AutoModel
import torch
import os
import sys

# Define paths
base_dir = "/Users/hardentie/Downloads/vscode"
model_dir = "/Users/hardentie/.cache/modelscope/hub/models/FunAudioLLM/Fun-ASR-Nano-2512"
repo_dir = os.path.join(base_dir, "Fun-ASR")
audio_file = os.path.join(base_dir, "庙后街 8.wav")
remote_code_path = os.path.join(repo_dir, "model.py")

# Check paths
if not os.path.exists(model_dir):
    print(f"Error: Model dir {model_dir} not found. Run download_model.py first.")
    # Fallback to model ID if local not found (will try to download again)
    model_dir = "FunAudioLLM/Fun-ASR-Nano-2512"
    
if not os.path.exists(remote_code_path):
    print(f"Error: Remote code {remote_code_path} not found.")
    sys.exit(1)

if not os.path.exists(audio_file):
    print(f"Error: Audio {audio_file} not found.")
    sys.exit(1)

# Select device
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

print(f"Loading model from {model_dir}...")
print(f"Using remote code from {remote_code_path}...")

try:
    # Append repo dir to sys.path just in case model.py imports other things from there
    sys.path.append(repo_dir)
    
    model = AutoModel(
        model=model_dir,
        trust_remote_code=True,
        remote_code=remote_code_path, # Use the cloned local file
        device=device,
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 60000},
        punc_model="ct-punc", 
    )
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Starting transcription...")
try:
    res = model.generate(
        input=audio_file,
        batch_size=1, 
        language="中文", # Fun-ASR supports autodetect or explicit
        itn=True,
    )
    
    full_text = ""
    # Result is usually a list of dicts: [{'key': '...', 'text': '...'}]
    if isinstance(res, list):
        for item in res:
            if 'text' in item:
                full_text += item['text']
            elif 'sentence' in item:
                 full_text += item['sentence']
    else:
        print("Result is not a list:", res)

    print("-" * 20)
    print(full_text[:500] + "...")
    
    with open("transcript_funasr.txt", "w", encoding='utf-8') as f:
        f.write(full_text)
    print("Saved to transcript_funasr.txt")

except Exception as e:
    print(f"Error during generation: {e}")
    import traceback
    traceback.print_exc()
