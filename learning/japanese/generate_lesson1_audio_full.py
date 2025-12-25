import asyncio
import os
import edge_tts

# Voice Definitions
VOICE_FEMALE_1 = "ja-JP-NanamiNeural"  # Standard Female
VOICE_MALE_1 = "ja-JP-KeitaNeural"    # Standard Male

# Output Directory
OUTPUT_DIR = "assets/audio/lesson1"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"Generated: {output_file}")

async def main():
    tasks = []

    # --- 1. Vocabulary ---
    vocab_list = [
        # Countries & Nationalities
        {"id": "chuugokujin", "text": "中国人", "voice": VOICE_FEMALE_1},
        {"id": "nihonjin", "text": "日本人", "voice": VOICE_FEMALE_1},
        {"id": "kankokujin", "text": "韓国人", "voice": VOICE_FEMALE_1},
        {"id": "amerikajin", "text": "アメリカ人", "voice": VOICE_FEMALE_1},
        {"id": "suisu", "text": "スイス", "voice": VOICE_FEMALE_1},
        {"id": "furansu", "text": "フランス", "voice": VOICE_FEMALE_1},
        
        # Roles
        {"id": "sensei", "text": "先生", "voice": VOICE_FEMALE_1},
        {"id": "gakusei", "text": "学生", "voice": VOICE_FEMALE_1},
        {"id": "ryuugakusei", "text": "留学生", "voice": VOICE_FEMALE_1},
        {"id": "kenkyuuin", "text": "研究員", "voice": VOICE_FEMALE_1},
        {"id": "daigaku", "text": "大学", "voice": VOICE_FEMALE_1},
        {"id": "kaishain", "text": "会社員", "voice": VOICE_FEMALE_1},
        {"id": "shain", "text": "社員", "voice": VOICE_FEMALE_1},
        {"id": "kyouju", "text": "教授", "voice": VOICE_FEMALE_1},
        {"id": "isha", "text": "医者", "voice": VOICE_FEMALE_1},
        {"id": "buchou", "text": "部長", "voice": VOICE_FEMALE_1},
        {"id": "kachou", "text": "課长", "voice": VOICE_FEMALE_1},

        # Family & People
        {"id": "chichi", "text": "父", "voice": VOICE_MALE_1},
        {"id": "haha", "text": "母", "voice": VOICE_FEMALE_1},
        {"id": "tomodachi", "text": "友達", "voice": VOICE_FEMALE_1},
        {"id": "hito", "text": "人", "voice": VOICE_FEMALE_1},
        {"id": "dare", "text": "誰", "voice": VOICE_FEMALE_1},
        {"id": "donata", "text": "どなた", "voice": VOICE_FEMALE_1},

        # Suffixes
        {"id": "san", "text": "さん", "voice": VOICE_FEMALE_1},
        {"id": "kun", "text": "君", "voice": VOICE_FEMALE_1},
        {"id": "chan", "text": "ちゃん", "voice": VOICE_FEMALE_1},
        {"id": "sama", "text": "様", "voice": VOICE_FEMALE_1},

        # Pronouns
        {"id": "watashi", "text": "私", "voice": VOICE_FEMALE_1},
        {"id": "anata", "text": "あなた", "voice": VOICE_FEMALE_1},
        {"id": "kare", "text": "彼", "voice": VOICE_FEMALE_1},
        {"id": "kanojo", "text": "彼女", "voice": VOICE_FEMALE_1},
        {"id": "ore", "text": "俺", "voice": VOICE_MALE_1},
        {"id": "boku", "text": "僕", "voice": VOICE_MALE_1},
        {"id": "atashi", "text": "あたし", "voice": VOICE_FEMALE_1},

        # Names
        {"id": "ri", "text": "李", "voice": VOICE_FEMALE_1},
        {"id": "ou", "text": "王", "voice": VOICE_FEMALE_1},
        {"id": "chou", "text": "張", "voice": VOICE_FEMALE_1},
        {"id": "mori", "text": "森", "voice": VOICE_FEMALE_1},
        {"id": "ono", "text": "小野", "voice": VOICE_FEMALE_1},
        {"id": "hayashi", "text": "林", "voice": VOICE_FEMALE_1},
        {"id": "yoshida", "text": "吉田", "voice": VOICE_FEMALE_1},
        {"id": "tanaka", "text": "田中", "voice": VOICE_FEMALE_1},
        {"id": "nakamura", "text": "中村", "voice": VOICE_FEMALE_1},
        {"id": "kimu", "text": "キム", "voice": VOICE_FEMALE_1},
        {"id": "dyupon", "text": "デュポン", "voice": VOICE_FEMALE_1},
        {"id": "sumisu", "text": "スミス", "voice": VOICE_FEMALE_1},
        {"id": "jonson", "text": "ジョンソン", "voice": VOICE_FEMALE_1},
    ]
    
    for item in vocab_list:
        tasks.append(generate_audio(item["text"], item["voice"], os.path.join(OUTPUT_DIR, f"{item['id']}.mp3")))

    # --- 2. Key Phrases ---
    phrases_list = [
        {"id": "hai_iie", "text": "はい。いいえ。", "voice": VOICE_FEMALE_1},
        {"id": "hajimemashite", "text": "はじめまして。", "voice": VOICE_FEMALE_1},
        {"id": "douzo", "text": "どうぞ。", "voice": VOICE_FEMALE_1},
        {"id": "yoroshiku", "text": "よろしくお願いします。", "voice": VOICE_FEMALE_1},
        {"id": "wakarimashita", "text": "分かりました。分かりません。", "voice": VOICE_FEMALE_1},
        {"id": "chigaimasu", "text": "違います。", "voice": VOICE_FEMALE_1},
    ]
    for item in phrases_list:
        tasks.append(generate_audio(item["text"], item["voice"], os.path.join(OUTPUT_DIR, f"{item['id']}.mp3")))

    # --- 3. Grammar Examples ---
    grammar_list = [
        {"id": "grammar_1_1", "text": "李さんは中国人です。", "voice": VOICE_FEMALE_1},
        {"id": "grammar_1_2", "text": "私は学生です。", "voice": VOICE_FEMALE_1},
        {"id": "grammar_2_1", "text": "森さんは学生じゃありません。", "voice": VOICE_FEMALE_1},
        {"id": "grammar_2_2", "text": "私はアメリカ人ではありません。", "voice": VOICE_FEMALE_1},
        {"id": "grammar_3_1", "text": "林さんは日本人ですか。", "voice": VOICE_FEMALE_1},
        {"id": "grammar_3_2", "text": "はい、そうです。", "voice": VOICE_FEMALE_1},
        {"id": "grammar_3_3", "text": "いいえ、違います。", "voice": VOICE_FEMALE_1},
        {"id": "grammar_4_1", "text": "J C企画の社員", "voice": VOICE_FEMALE_1},
        {"id": "grammar_4_2", "text": "日本語の学生", "voice": VOICE_FEMALE_1},
        {"id": "grammar_4_3", "text": "李さんはJ C企画の社員です。", "voice": VOICE_FEMALE_1},
    ]
    for item in grammar_list:
        tasks.append(generate_audio(item["text"], item["voice"], os.path.join(OUTPUT_DIR, f"{item['id']}.mp3")))

    # --- 4. Text / Dialogues ---
    dialogues = [
        # Scene 1
        {"id": "text_1_1", "text": "J C企画の小野さんですか。", "voice": VOICE_FEMALE_1}, # Li (Female)
        {"id": "text_1_2", "text": "はい、小野です。李さんですか。", "voice": VOICE_FEMALE_1}, # Ono
        {"id": "text_1_3", "text": "はい、李です。はじめまして。", "voice": VOICE_FEMALE_1}, # Li (Female)
        {"id": "text_1_4", "text": "はじめまして、小野あつこです。よろしくお願いします。", "voice": VOICE_FEMALE_1}, # Ono

        # Scene 2
        {"id": "text_2_1", "text": "吉田さんですか。", "voice": VOICE_FEMALE_1}, # Li (Female)
        {"id": "text_2_2", "text": "いいえ、吉田じゃありません。森です。", "voice": VOICE_MALE_1}, # Mori (Male)
        {"id": "text_2_3", "text": "あ、森さんですか。どうもすみません。", "voice": VOICE_FEMALE_1}, # Li (Female)
        {"id": "text_2_4", "text": "いいえ。どうぞよろしくお願いします。", "voice": VOICE_MALE_1}, # Mori (Male)
        {"id": "text_2_5", "text": "李秀麗です。こちらこそ。", "voice": VOICE_FEMALE_1}, # Li (Female)

        # Scene 3 (Narrator & Dialogues)
        {"id": "scene3_narrator", "text": "ハイ、はじめまして！私は田中です。日本人です。これは父と母です。あの人は友達の林くんです。彼は学生じゃありません。会社員です。社員です。", "voice": VOICE_FEMALE_1}, # Tanaka (Female?) "Watashi" used. Let's use Female.

        {"id": "scene3_dialogue1_q", "text": "あの方（かた）はどなたですか。", "voice": VOICE_FEMALE_1},
        {"id": "scene3_dialogue1_a", "text": "中村教授です。大学の先生です。彼女は森ちゃんです。", "voice": VOICE_FEMALE_1}, # Mmm "Mori-chan"? implies female then. Okay.

        {"id": "scene3_dialogue2_boys", "text": "俺は元気です。僕も元気です。", "voice": VOICE_MALE_1},
        {"id": "scene3_dialogue2_girl", "text": "あたしは小野です。", "voice": VOICE_FEMALE_1},

        {"id": "scene3_dialogue3_qa", "text": "小野さん、あなたは部長ですか？いいえ、違います。課長です。じゃ、誰が部長ですか？吉田様です。", "voice": VOICE_FEMALE_1}, # Combined Q&A

        {"id": "scene3_closing", "text": "どうぞよろしくお願いします！", "voice": VOICE_FEMALE_1},
    ]
    for item in dialogues:
        tasks.append(generate_audio(item["text"], item["voice"], os.path.join(OUTPUT_DIR, f"{item['id']}.mp3")))

    print(f"Generating {len(tasks)} audio files...")
    await asyncio.gather(*tasks)
    print("All audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
