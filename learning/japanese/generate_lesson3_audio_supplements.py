
import os
import asyncio
import edge_tts

async def generate_audio(text, output_file, voice="ja-JP-NanamiNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"Generated: {output_file}")

async def main():
    base_dir = "/Users/hardentie/Downloads/vscode/learning/japanese/assets/audio/lesson3"
    os.makedirs(base_dir, exist_ok=True)

    # Vocabulary
    vocab_data = [
        {"word": "トイレ", "kana": "といれ"},
        {"word": "お手洗い", "kana": "おてあらい"},
        {"word": "隣", "kana": "となり"},
        {"word": "周辺", "kana": "しゅうへん"},
        {"word": "今日", "kana": "きょう"},
        {"word": "水曜日", "kana": "すいようび"},
        {"word": "木曜日", "kana": "もくようび"},
        {"word": "いくら", "kana": "いくら"},
        {"word": "こちら", "kana": "こちら"},
        {"word": "そちら", "kana": "そちら"},
        {"word": "あちら", "kana": "あちら"},
        {"word": "どちら", "kana": "どちら"},
    ]

    # Grammar Examples
    grammar_data = [
        # Polite Place Pronouns
        {"id": "grammar_6_1", "text": "こちらは田中さんです。"},
        {"id": "grammar_6_2", "text": "お手洗いはあちらです。"},
        
        # Particle Mo
        {"id": "grammar_7_1", "text": "私は中国人です。周さんも中国人です。"},
        {"id": "grammar_7_2", "text": "これも日本のペンですね。"},
        
        # Choice Questions (combining Q and A with a pause if possible, but edge-tts doesn't support pause directly in simple text. 
        # We'll just concatenate with a period or space which usually adds a slight pause.)
        {"id": "grammar_8_1", "text": "今日は水曜日ですか、木曜日ですか。水曜日です。"},
        {"id": "grammar_8_2", "text": "ここは一階ですか、二階ですか。二階です。"},
        
        # Asking Price
        {"id": "grammar_9_1", "text": "このかばんはいくらですか。五千八百円です。"},
    ]

    tasks = []

    # Generate Vocab Audio
    for item in vocab_data:
        filename = f"vocab_{item['word']}.mp3"
        filepath = os.path.join(base_dir, filename)
        # Use the word itself for audio
        text = item['word']
        tasks.append(generate_audio(text, filepath))

    # Generate Grammar Audio
    for item in grammar_data:
        filename = f"{item['id']}.mp3"
        filepath = os.path.join(base_dir, filename)
        tasks.append(generate_audio(item['text'], filepath))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
