import asyncio
import os
import edge_tts

# OUTPUT DIRECTORY
output_dir = "assets/audio/lesson2"
os.makedirs(output_dir, exist_ok=True)

# VOICES
VOICE_FEMALE_1 = "ja-JP-NanamiNeural" # Standard Female
VOICE_FEMALE_2 = "ja-JP-MayuNeural"   # Soft Female (or pitch adjusted Nanami)
VOICE_MALE_1 = "ja-JP-KeitaNeural"    # Standard Male

# DATA
# Structure: {'id': 'filename_without_ext', 'text': 'Japanese text', 'voice': 'voice_var'}

vocab_list = [
    # Items
    {"id": "hon", "text": "本", "voice": VOICE_FEMALE_1},
    {"id": "kaban", "text": "鞄", "voice": VOICE_FEMALE_1},
    {"id": "enpitsu", "text": "鉛筆", "voice": VOICE_FEMALE_1},
    {"id": "kasa", "text": "傘", "voice": VOICE_FEMALE_1},
    {"id": "kutsu", "text": "靴", "voice": VOICE_FEMALE_1},
    {"id": "shinbun", "text": "新聞", "voice": VOICE_FEMALE_1},
    
    # Electronics
    {"id": "pasokon", "text": "パソコン", "voice": VOICE_FEMALE_1},
    {"id": "kamera", "text": "カメラ", "voice": VOICE_FEMALE_1},
    {"id": "terebi", "text": "テレビ", "voice": VOICE_FEMALE_1},
    {"id": "nyuusu", "text": "ニュース", "voice": VOICE_FEMALE_1},
    
    # Furniture
    {"id": "tsukue", "text": "机", "voice": VOICE_FEMALE_1},
    {"id": "isu", "text": "椅子", "voice": VOICE_FEMALE_1},
    {"id": "kagi", "text": "鍵", "voice": VOICE_FEMALE_1},
    {"id": "tokei", "text": "時計", "voice": VOICE_FEMALE_1},
    {"id": "techou", "text": "手帳", "voice": VOICE_FEMALE_1},
    {"id": "shashin", "text": "写真", "voice": VOICE_FEMALE_1},
    
    # Vehicles & Gifts
    {"id": "kuruma", "text": "車", "voice": VOICE_FEMALE_1},
    {"id": "jitensha", "text": "自転車", "voice": VOICE_FEMALE_1},
    {"id": "omiyage", "text": "お土産", "voice": VOICE_FEMALE_1},
    {"id": "meisanhin", "text": "名産品", "voice": VOICE_FEMALE_1},
    {"id": "shiruku", "text": "シルク", "voice": VOICE_FEMALE_1},
    {"id": "hankachi", "text": "ハンカチ", "voice": VOICE_FEMALE_1},
    {"id": "jidousha", "text": "自動車", "voice": VOICE_FEMALE_1},
    {"id": "purezento", "text": "プレゼント", "voice": VOICE_FEMALE_1},
    
    # People
    {"id": "kaisha", "text": "会社", "voice": VOICE_FEMALE_1},
    {"id": "kata", "text": "方", "voice": VOICE_FEMALE_1},
    {"id": "hito", "text": "人", "voice": VOICE_FEMALE_1},
    {"id": "haha", "text": "母", "voice": VOICE_FEMALE_1},
    {"id": "kazoku", "text": "家族", "voice": VOICE_FEMALE_1},
    
    # Supplementary
    {"id": "baggu", "text": "バッグ", "voice": VOICE_FEMALE_1},
    {"id": "kutsushita", "text": "靴下", "voice": VOICE_FEMALE_1},
    {"id": "keitai", "text": "ケータイ", "voice": VOICE_FEMALE_1},
    {"id": "teeburu", "text": "テーブル", "voice": VOICE_FEMALE_1},
    {"id": "udedokei", "text": "腕時計", "voice": VOICE_FEMALE_1},
    {"id": "manga", "text": "漫画", "voice": VOICE_FEMALE_1},
    {"id": "kyoukasho", "text": "教科書", "voice": VOICE_FEMALE_1},
    {"id": "tegami", "text": "手紙", "voice": VOICE_FEMALE_1},
    {"id": "kaishain", "text": "会社員", "voice": VOICE_FEMALE_1},
    {"id": "okaasan", "text": "お母さん", "voice": VOICE_FEMALE_1},
    {"id": "shiruku_no_hankachi", "text": "シルクのハンカチ", "voice": VOICE_FEMALE_1},
    {"id": "nagashima", "text": "長島", "voice": VOICE_FEMALE_1},
    {"id": "nouto", "text": "ノート", "voice": VOICE_FEMALE_1},
    {"id": "borupen", "text": "ボールペン", "voice": VOICE_FEMALE_1},
    {"id": "shaapupenshiru", "text": "シャープペンシル", "voice": VOICE_FEMALE_1},

    # Numbers
    {"id": "zero", "text": "ゼロ", "voice": VOICE_FEMALE_1},
    {"id": "ichi", "text": "いち", "voice": VOICE_FEMALE_1},
    {"id": "ni", "text": "に", "voice": VOICE_FEMALE_1},
    {"id": "san", "text": "さん", "voice": VOICE_FEMALE_1},
    {"id": "yon", "text": "よん", "voice": VOICE_FEMALE_1},
    {"id": "go", "text": "ご", "voice": VOICE_FEMALE_1},
    {"id": "roku", "text": "ろく", "voice": VOICE_FEMALE_1},
    {"id": "nana", "text": "なな", "voice": VOICE_FEMALE_1},
    {"id": "hachi", "text": "はち", "voice": VOICE_FEMALE_1},
    {"id": "kyuu", "text": "きゅう", "voice": VOICE_FEMALE_1},
    {"id": "juu", "text": "じゅう", "voice": VOICE_FEMALE_1},
    {"id": "hyaku", "text": "ひゃく", "voice": VOICE_FEMALE_1},
]

grammar_list = [
    # Pattern 1
    {"id": "gram_01_1", "text": "これは本です。", "voice": VOICE_FEMALE_1},
    {"id": "gram_01_2", "text": "それは鞄です。", "voice": VOICE_FEMALE_1},
    
    # Pattern 2 (Kono)
    {"id": "gram_02_1", "text": "このカメラはスミスのです。", "voice": VOICE_FEMALE_1},
    
    # Pattern 3 (No)
    {"id": "gram_03_1", "text": "私の本", "voice": VOICE_FEMALE_1},
    {"id": "gram_03_2", "text": "日本語の先生", "voice": VOICE_FEMALE_1},
    {"id": "gram_03_3", "text": "中国のお土産", "voice": VOICE_FEMALE_1},
    {"id": "gram_03_4", "text": "それは私のです。", "voice": VOICE_FEMALE_1},
    
    # Pattern 4 (Questions)
    {"id": "gram_04_1", "text": "それは辞書ですか。", "voice": VOICE_FEMALE_1},
    {"id": "gram_04_2", "text": "はい、そうです。", "voice": VOICE_FEMALE_1},
    {"id": "gram_04_3", "text": "いいえ、違います。", "voice": VOICE_FEMALE_1},
    
    # Pattern 5 (Special Qs)
    {"id": "gram_05_1", "text": "森さんの鞄はどれですか。", "voice": VOICE_FEMALE_1},
    {"id": "gram_05_2", "text": "あの方はどなたですか。", "voice": VOICE_FEMALE_1},
]

expressions = [
    {"id": "expr_douzo", "text": "どうぞ", "voice": VOICE_FEMALE_1},
    {"id": "expr_doumo", "text": "どうも", "voice": VOICE_FEMALE_1},
    {"id": "expr_oikutsu", "text": "おいくつですか", "voice": VOICE_FEMALE_1},
    {"id": "expr_nansai", "text": "何歳ですか", "voice": VOICE_FEMALE_1},
]

dialogues = [
    # Basic
    {"id": "basic_1_a", "text": "これはテレビですか。", "voice": VOICE_MALE_1},
    {"id": "basic_1_b", "text": "いいえ、それはテレビではありません。パソコンです。", "voice": VOICE_FEMALE_1},
    {"id": "basic_2_a", "text": "それは何ですか。", "voice": VOICE_FEMALE_1},
    {"id": "basic_2_b", "text": "これは日本語の本です。", "voice": VOICE_MALE_1},
    {"id": "basic_3_a", "text": "森さんの鞄はどれですか。", "voice": VOICE_MALE_1},
    {"id": "basic_3_b", "text": "あの鞄です。", "voice": VOICE_FEMALE_1},
    {"id": "basic_4_a", "text": "そのノートは誰のですか。", "voice": VOICE_FEMALE_1},
    {"id": "basic_4_b", "text": "私のです。", "voice": VOICE_MALE_1},
    
    # Scene 1
    {"id": "scene1_1", "text": "李さん、それは何ですか。", "voice": VOICE_MALE_1}, # Tanaka
    {"id": "scene1_2", "text": "これですか。これは家族の写真です。", "voice": VOICE_FEMALE_1}, # Li
    {"id": "scene1_3", "text": "この方はどなたですか。", "voice": VOICE_MALE_1}, # Tanaka
    {"id": "scene1_4", "text": "私の母です。", "voice": VOICE_FEMALE_1}, # Li
    {"id": "scene1_5", "text": "お母さんはおいくつですか。", "voice": VOICE_MALE_1}, # Tanaka
    {"id": "scene1_6", "text": "52歳です。", "voice": VOICE_FEMALE_1}, # Li

    # Scene 2
    {"id": "scene2_1", "text": "小野さん、これ、どうぞ。", "voice": VOICE_FEMALE_1}, # Li
    {"id": "scene2_2", "text": "えっ、これは何ですか。", "voice": VOICE_FEMALE_1}, # Ono (Using same Fem voice for now, or could change pitch)
    {"id": "scene2_3", "text": "お土産です。シルクのハンカチです。", "voice": VOICE_FEMALE_1}, # Li
    {"id": "scene2_4", "text": "わあ、スワトウのハンカチですか。", "voice": VOICE_FEMALE_1}, # Ono
    {"id": "scene2_5", "text": "ええ。中国の名産品です。", "voice": VOICE_FEMALE_1}, # Li
    {"id": "scene2_6", "text": "どうもありがとうございます。", "voice": VOICE_FEMALE_1}, # Ono
]

practice = [
    # Answers only
    {"id": "ex_1", "text": "これはパソコンです。", "voice": VOICE_FEMALE_1},
    {"id": "ex_2", "text": "それは何ですか。", "voice": VOICE_FEMALE_1},
    {"id": "ex_3", "text": "この傘は私のです。", "voice": VOICE_FEMALE_1},
    {"id": "ex_4", "text": "尖閣諸島は中国のです。蒼井空は世界のです。", "voice": VOICE_FEMALE_1},
    {"id": "ex_5", "text": "それは森さんの本ではありません。", "voice": VOICE_FEMALE_1}, # Subst 1
    {"id": "ex_5b", "text": "それは森さんのテレビではありません。", "voice": VOICE_FEMALE_1}, # Subst 2
    {"id": "ex_6_a", "text": "それ は なん です か。", "voice": VOICE_FEMALE_1},
    {"id": "ex_6_b", "text": "これはテレビです。", "voice": VOICE_FEMALE_1},
    {"id": "ex_7", "text": "これは誰の傘ですか。", "voice": VOICE_FEMALE_1},
    {"id": "ex_8", "text": "あの人は誰ですか。", "voice": VOICE_FEMALE_1},
    {"id": "ex_9", "text": "なん", "voice": VOICE_FEMALE_1},
    {"id": "ex_10", "text": "は", "voice": VOICE_FEMALE_1},
    {"id": "ex_11_a", "text": "いいえ、私のではありません。", "voice": VOICE_FEMALE_1},
    {"id": "ex_11_b", "text": "それは私のです。", "voice": VOICE_FEMALE_1},
    {"id": "ex_12", "text": "あれは誰の傘ですか。", "voice": VOICE_FEMALE_1},
]

full_list = vocab_list + grammar_list + expressions + dialogues + practice

async def main():
    print(f"Generating {len(full_list)} audio files for Lesson 2...")
    
    semaphore = asyncio.Semaphore(5) # Limit concurrent connections

    async def generate(item):
        async with semaphore:
            output_path = f"{output_dir}/{item['id']}.mp3"
            if os.path.exists(output_path):
                # Optional: Skip if exists to save time
                # print(f"Skipping {item['id']} (exists)")
                # return
                pass

            print(f"Generating {item['id']}...")
            try:
                communicate = edge_tts.Communicate(item["text"], item["voice"])
                await communicate.save(output_path)
            except Exception as e:
                print(f"Error {item['id']}: {e}")

    # Run in batches
    tasks = [generate(item) for item in full_list]
    await asyncio.gather(*tasks)

    print("All audio generated!")

if __name__ == "__main__":
    asyncio.run(main())
