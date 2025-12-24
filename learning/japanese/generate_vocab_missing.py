import asyncio
import os
import edge_tts

# Ensure directory exists
output_dir = "assets/audio/lesson1"
os.makedirs(output_dir, exist_ok=True)

# Standard Voice for Vocab
VOICE = "ja-JP-NanamiNeural"

vocab_list = [
    # Missing words
    {"id": "donata", "text": "どなた"},
    {"id": "kare", "text": "彼"},
    {"id": "kanojo", "text": "彼女"},
    
    # Names
    {"id": "ri", "text": "李"},
    {"id": "ou", "text": "王"},
    {"id": "chou", "text": "張"},
    {"id": "mori", "text": "森"},
    {"id": "ono", "text": "小野"},
    {"id": "hayashi", "text": "林"},
    {"id": "yoshida", "text": "吉田"},
    {"id": "tanaka", "text": "田中"},
    {"id": "nakamura", "text": "中村"},
    {"id": "kimu", "text": "キム"},
    {"id": "dyupon", "text": "デュポン"},
    {"id": "sumisu", "text": "スミス"},
    {"id": "jonson", "text": "ジョンソン"},

    # Key Phrases
    {"id": "hai_iie", "text": "はい、いいえ"},
    {"id": "douzo", "text": "どうぞ"},
    {"id": "yoroshiku", "text": "よろしくお願いします"},
    {"id": "wakarimashita", "text": "分かりました"},
    {"id": "chigaimasu", "text": "違います"},
]

async def main():
    print("Generating missing vocabulary audio files...")
    for item in vocab_list:
        output_path = f"{output_dir}/{item['id']}.mp3"
        print(f"Generating {output_path}...")
        try:
            communicate = edge_tts.Communicate(item["text"], VOICE)
            await communicate.save(output_path)
            # Small delay to keep it stable
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error generating {item['id']}: {e}")
    print("Missing vocabulary audio generation complete!")

if __name__ == "__main__":
    asyncio.run(main())
