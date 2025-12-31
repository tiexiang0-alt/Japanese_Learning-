from modelscope import snapshot_download

print("Downloading model...")
try:
    model_dir = snapshot_download('FunAudioLLM/Fun-ASR-Nano-2512')
    print(f"Model downloaded to: {model_dir}")
except Exception as e:
    print(f"Download failed: {e}")
