import asyncio
import os
import edge_tts

# Ensure directory exists
output_dir = "assets/audio/lesson1"
os.makedirs(output_dir, exist_ok=True)

# Voices
VOICE_FEMALE = "ja-JP-NanamiNeural"
VOICE_MALE = "ja-JP-KeitaNeural"

# Scene 03 Content
audio_segments = [
    {
        "id": "scene3_narrator",
        "text": "ハイ、はじめまして！私は田中です。日本人です。これは父と母です。あの人は友達の林君です。彼は学生じゃありません。会社員です。社員です。",
        "voice": VOICE_FEMALE
    },
    {
        "id": "scene3_dialogue1_q",
        "text": "あの方はどなたですか。",
        "voice": VOICE_FEMALE
    },
    {
        "id": "scene3_dialogue1_a",
        "text": "中村教授です。大学の先生です。彼女は森ちゃんです。",
        "voice": VOICE_MALE
    },
    {
        "id": "scene3_dialogue2_boys",
        "text": "俺は元気です。僕も元気です。",
        "voice": VOICE_MALE
    },
    {
        "id": "scene3_dialogue2_girl",
        "text": "あたしは小野です。",
        "voice": VOICE_FEMALE
    },
    {
        "id": "scene3_dialogue3_qa",
        "text": "小野さん、あなたは部長ですか？ いいえ、違います。課長です。 じゃ、誰が部長ですか？ 吉田様です。",
        "voice": VOICE_FEMALE
    },
    {
         "id": "scene3_closing",
         "text": "はい、分かりました。どうぞ よろしく お願いします！",
         "voice": VOICE_FEMALE
    }
]


async def generate_audio():
    print(f"Generating {len(audio_segments)} audio files for Scene 03...")
    
    for item in audio_segments:
        output_file = os.path.join(output_dir, f"{item['id']}.mp3")
        communicate = edge_tts.Communicate(item['text'], item['voice'])
        await communicate.save(output_file)
        print(f"✅ Generated: {output_file}")

if __name__ == "__main__":
    asyncio.run(generate_audio())
