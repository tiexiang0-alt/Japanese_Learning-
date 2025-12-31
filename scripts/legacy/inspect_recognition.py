import dashscope
from dashscope.audio.asr import Recognition

print("Recognition Attributes:")
print(dir(Recognition))

try:
    print("Recognition.call doc:")
    print(Recognition.call.__doc__)
except:
    pass
