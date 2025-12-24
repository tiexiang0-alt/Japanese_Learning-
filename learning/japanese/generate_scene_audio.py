import asyncio
import os
import edge_tts

# Ensure directory exists
output_dir = "assets/audio/lesson1"
os.makedirs(output_dir, exist_ok=True)

# Available Voices: ja-JP-KeitaNeural, ja-JP-NanamiNeural

# Character Configuration
CHARACTERS = {
    "Li": {"voice": "ja-JP-KeitaNeural", "pitch": "+0Hz"},
    "Ono": {"voice": "ja-JP-NanamiNeural", "pitch": "+0Hz"},
    "Yoshida": {"voice": "ja-JP-NanamiNeural", "pitch": "-20Hz"}, # Slightly deeper female voice
    "Mori": {"voice": "ja-JP-KeitaNeural", "pitch": "-10Hz"},   # Slightly deeper male voice
}

lines = [
    # Scene 1
    {"id": "text_1_1", "text": "JC企画の小野さんですか。", "char": "Li"},
    {"id": "text_1_2", "text": "はい、小野です。李さんですか。", "char": "Ono"},
    {"id": "text_1_3", "text": "はい、李です。はじめまして。", "char": "Li"},
    {"id": "text_1_4", "text": "はじめまして、小野あつこです。よろしくお願いします。", "char": "Ono"},
    
    # Scene 2
    {"id": "text_2_1", "text": "李さんですか。", "char": "Yoshida"},
    {"id": "text_2_2", "text": "いいえ、李じゃありません。森です。", "char": "Mori"},
    {"id": "text_2_3", "text": "あ、すいません。人違いでした。", "char": "Yoshida"},
]

async def main():
    print("Generating audio files...")
    for line in lines:
        output_path = f"{output_dir}/{line['id']}.mp3"
        char_config = CHARACTERS[line["char"]]
        print(f"Generating {output_path} ({line['char']})...")
        
        try:
            communicate = edge_tts.Communicate(
                line["text"], 
                char_config["voice"], 
                pitch=char_config["pitch"]
            )
            await communicate.save(output_path)
        except Exception as e:
            print(f"Error generating {line['id']}: {e}")

    print("Audio generation complete!")

if __name__ == "__main__":
    asyncio.run(main())
