import dashscope
import pkgutil

print("DashScope version:", dashscope.__version__)
print("Submodules:")
for loader, module_name, is_pkg in pkgutil.walk_packages(dashscope.__path__):
    print(module_name)

print("\nAttributes:")
print(dir(dashscope))
print("\nAudio attributes:")
try:
    from dashscope.audio import asr
    print(dir(asr))
    print(dir(asr.Transcription))
except ImportError:
    print("Could not import dashscope.audio.asr")
