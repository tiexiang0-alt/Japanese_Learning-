import asyncio
import os
import edge_tts

# Ensure directory exists
output_dir = "assets/audio/lesson1"
os.makedirs(output_dir, exist_ok=True)

# Standard Voice for Vocab
VOICE = "ja-JP-NanamiNeural"

vocab_list = [
    # Resuming from Buchou
    {"id": "buchou", "text": "部長"},
    {"id": "kachou", "text": "課長"},

    # Family & People
    {"id": "chichi", "text": "父"},
    {"id": "haha", "text": "母"},
    {"id": "tomodachi", "text": "友達"},
    {"id": "hito", "text": "人"},
    {"id": "dare", "text": "誰"},
    {"id": "donata", "text": "どなた"},

    # Honorifics
    {"id": "san", "text": "さん"},
    {"id": "kun", "text": "くん"},
    {"id": "chan", "text": "ちゃん"},
    {"id": "sama", "text": "様"},

    # Pronouns
    {"id": "watashi", "text": "私"},
    {"id": "anata", "text": "あなた"},
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
    {"id": "hajimemashite", "text": "はじめまして"},
    {"id": "douzo", "text": "どうぞ"},
    {"id": "yoroshiku", "text": "よろしくお願いします"},
    {"id": "wakarimashita", "text": "分かりました"},
    {"id": "chigaimasu", "text": "違います"},
]

async def main():
    print("Resuming vocabulary audio generation...")
    for item in vocab_list:
        output_path = f"{output_dir}/{item['id']}.mp3"
        print(f"Generating {output_path}...")
        try:
            communicate = edge_tts.Communicate(item["text"], VOICE)
            await communicate.save(output_path)
            # Add a small delay to avoid rate limits/network congestion
            await asyncio.sleep(1) 
        except Exception as e:
            print(f"Error generating {item['id']}: {e}")
    print("Vocabulary audio generation complete!")

if __name__ == "__main__":
    asyncio.run(main())
