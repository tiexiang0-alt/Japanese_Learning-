from funasr import AutoModel
import torch
import os

# Define model and file
model_dir = "FunAudioLLM/Fun-ASR-Nano-2512"
audio_file = "/Users/hardentie/Downloads/vscode/庙后街 8.m4a"

# Check file
if not os.path.exists(audio_file):
    print(f"Error: File {audio_file} not found.")
    exit(1)

# Select device
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

print(f"Loading model {model_dir}...")
try:
    model = AutoModel(
        model=model_dir,
        trust_remote_code=True,
        device=device,
        # vad_model="fsmn-vad", # Optional: add VAD for long audio if needed, usually AutoModel handles basics?
        # The user example showed two usages, one with VAD. 
        # For a meeting recording (long audio), VAD is highly recommended to split segments.
        # Let's include basic VAD config as per docs/examples if possible, or just defaults.
        # The default AutoModel might not include VAD unless specified? 
        # Fun-ASR usually integrates them. Let's try basic first or add VAD if it's a "meeting".
        # User said "conference/meeting", so VAD is important.
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 60000},
        punc_model="ct-punc", 
        # spk_model="cam++", # Optional speaker diarization? User didn't explicitly ask but it's a meeting.
    )
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

print("Starting transcription...")
try:
    res = model.generate(
        input=audio_file,
        batch_size=1, # sequential for safety
        language="中文", 
        itn=True, # Inverse Text Normalization (numbers to digits etc)
        # hotwords=["河南话"], # Maybe helpful?
    )
    
    # print(res)
    
    # Extract text
    # Result structure is list of dicts?
    full_text = ""
    if isinstance(res, list):
        for item in res:
            if 'text' in item:
                full_text += item['text'] + "\n"
    else:
        print("Unexpected result format:", res)

    print("-" * 20)
    print(full_text[:500] + "...")
    
    with open("transcript_funasr.txt", "w", encoding='utf-8') as f:
        f.write(full_text)
    print("Saved to transcript_funasr.txt")

except Exception as e:
    print(f"Error during generation: {e}")
    import traceback
    traceback.print_exc()
