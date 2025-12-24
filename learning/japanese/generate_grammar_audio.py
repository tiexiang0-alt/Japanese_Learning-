import asyncio
import os
import edge_tts

# Ensure directory exists
output_dir = "assets/audio/lesson1"
os.makedirs(output_dir, exist_ok=True)

# Voices
VOICE_MALE = "ja-JP-KeitaNeural"
VOICE_FEMALE = "ja-JP-NanamiNeural"

lines = [
    # Grammar 1: Affirmative
    {"id": "grammar_1_1", "text": "李さんは中国人です。", "voice": VOICE_MALE},
    {"id": "grammar_1_2", "text": "私は学生です。", "voice": VOICE_FEMALE}, # Extra example

    # Grammar 2: Negative
    {"id": "grammar_2_1", "text": "森さんは学生じゃありません。", "voice": VOICE_MALE},
    {"id": "grammar_2_2", "text": "私はアメリカ人ではありません。", "voice": VOICE_FEMALE}, # Extra formal example

    # Grammar 3: Question
    {"id": "grammar_3_1", "text": "林さんは日本人ですか。", "voice": VOICE_FEMALE},
    {"id": "grammar_3_2", "text": "はい、そうです。", "voice": VOICE_MALE}, # Answer example
    {"id": "grammar_3_3", "text": "いいえ、違います。", "voice": VOICE_MALE}, # Answer example

    # Grammar 4: Particle 'no'
    {"id": "grammar_4_1", "text": "JS企画の社員", "voice": VOICE_FEMALE},
    {"id": "grammar_4_2", "text": "日本語の学生", "voice": VOICE_MALE},
    {"id": "grammar_4_3", "text": "李さんはJS企画の社員です。", "voice": VOICE_FEMALE}, # Full sentence example
]

async def main():
    print("Generating grammar audio files...")
    for line in lines:
        output_path = f"{output_dir}/{line['id']}.mp3"
        print(f"Generating {output_path}...")
        try:
            communicate = edge_tts.Communicate(line["text"], line["voice"])
            await communicate.save(output_path)
        except Exception as e:
            print(f"Error generating {line['id']}: {e}")
    print("Grammar audio generation complete!")

if __name__ == "__main__":
    asyncio.run(main())
