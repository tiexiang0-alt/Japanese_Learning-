import dashscope
import pkgutil

print("Attributes:")
print(dir(dashscope))

print("\nAudio ASR attributes:")
try:
    from dashscope.audio import asr
    print(dir(asr))
    if hasattr(asr, 'Transcription'):
        print(dir(asr.Transcription))
except ImportError:
    print("Could not import dashscope.audio.asr")

print("\nChecking for file upload capability:")
try:
    if hasattr(dashscope, 'file'):
        print(dir(dashscope.file))
    else:
        print("No dashscope.file")
except:
    pass
