import json
import random

# Lesson 2 Content Data
VOCAB = [
    {"kanji": "本", "kana": "ほん", "meaning": "Book", "type": "noun"},
    {"kanji": "辞書", "kana": "じしょ", "meaning": "Dictionary", "type": "noun"},
    {"kanji": "雑誌", "kana": "ざっし", "meaning": "Magazine", "type": "noun"},
    {"kanji": "新聞", "kana": "しんぶん", "meaning": "Newspaper", "type": "noun"},
    {"kanji": "ノート", "kana": "ノート", "meaning": "Notebook", "type": "noun"},
    {"kanji": "手帳", "kana": "てちょう", "meaning": "Pocket Notebook", "type": "noun"},
    {"kanji": "名刺", "kana": "めいし", "meaning": "Business Card", "type": "noun"},
    {"kanji": "カード", "kana": "カード", "meaning": "Card", "type": "noun"},
    {"kanji": "鉛筆", "kana": "えんぴつ", "meaning": "Pencil", "type": "noun"},
    {"kanji": "ボールペン", "kana": "ボールペン", "meaning": "Ballpoint Pen", "type": "noun"},
    {"kanji": "鍵", "kana": "かぎ", "meaning": "Key", "type": "noun"},
    {"kanji": "時計", "kana": "とけい", "meaning": "Watch/Clock", "type": "noun"},
    {"kanji": "傘", "kana": "かさ", "meaning": "Umbrella", "type": "noun"},
    {"kanji": "鞄", "kana": "かばん", "meaning": "Bag", "type": "noun"},
    {"kanji": "椅子", "kana": "いす", "meaning": "Chair", "type": "noun"},
    {"kanji": "机", "kana": "つくえ", "meaning": "Desk", "type": "noun"},
    {"kanji": "お土産", "kana": "おみやげ", "meaning": "Souvenir", "type": "noun"},
    {"kanji": "車", "kana": "くるま", "meaning": "Car", "type": "noun"},
    {"kanji": "自転車", "kana": "じてんしゃ", "meaning": "Bicycle", "type": "noun"},
    {"kanji": "カメラ", "kana": "カメラ", "meaning": "Camera", "type": "noun"},
    {"kanji": "パソコン", "kana": "パソコン", "meaning": "PC", "type": "noun"},
    {"kanji": "ラジオ", "kana": "ラジオ", "meaning": "Radio", "type": "noun"},
    {"kanji": "テレビ", "kana": "テレビ", "meaning": "TV", "type": "noun"},
    {"kanji": "英語", "kana": "えいご", "meaning": "English Language", "type": "noun"},
    {"kanji": "日本語", "kana": "にほんご", "meaning": "Japanese Language", "type": "noun"},
    {"kanji": "語", "kana": "ご", "meaning": "Language (suffix)", "type": "suffix"},
    {"kanji": "何", "kana": "なん", "meaning": "What", "type": "pronoun"},
    {"kanji": "そう", "kana": "そう", "meaning": "So/True", "type": "exp"},
    {"kanji": "コーヒー", "kana": "コーヒー", "meaning": "Coffee", "type": "noun"},
    {"kanji": "チョコレート", "kana": "チョコレート", "meaning": "Chocolate", "type": "noun"}
]

GRAMMAR_PATTERNS = [
    {
        "pattern": "Kore/Sore/Are",
        "description": "Demonstratives behaving as nouns",
        "questions": [
            {"q": "( &nbsp;&nbsp; ) は 本です。", "a": "これ", "options": ["これ", "その", "あの", "どの"]},
            {"q": "( &nbsp;&nbsp; ) は 私の 傘です。", "a": "それ", "options": ["それ", "その", "この", "どの"]},
            {"q": "( &nbsp;&nbsp; ) は 誰の 鞄ですか。", "a": "あれ", "options": ["あれ", "あの", "その", "どの"]}
        ]
    },
    {
        "pattern": "Kono/Sono/Ano + Noun",
        "description": "Demonstratives modifying nouns",
        "questions": [
            {"q": "( &nbsp;&nbsp; ) 本は 私のです。", "a": "この", "options": ["この", "これ", "それ", "あれ"]},
            {"q": "( &nbsp;&nbsp; ) 鞄は あなたのですか。", "a": "その", "options": ["その", "それ", "これ", "あれ"]},
            {"q": "( &nbsp;&nbsp; ) 人は 誰ですか。", "a": "あの", "options": ["あの", "あれ", "それ", "これ"]}
        ]
    },
    {
        "pattern": "Possession (No)",
        "description": "Particle 'no' for possession",
        "questions": [
            {"q": "これは 私( &nbsp;&nbsp; ) 本です。", "a": "の", "options": ["の", "は", "か", "も"]},
            {"q": "それは 田中さん( &nbsp;&nbsp; ) 傘ですか。", "a": "の", "options": ["の", "は", "に", "を"]},
            {"q": "あれは 日本語( &nbsp;&nbsp; ) 先生です。", "a": "の", "options": ["の", "が", "は", "も"]}
        ]
    },
    {
        "pattern": "Question (Nan)",
        "description": "Asking 'What'",
        "questions": [
            {"q": "これは ( &nbsp;&nbsp; ) ですか。", "a": "何", "options": ["何", "誰", "どこ", "いつ"]},
            {"q": "それは ( &nbsp;&nbsp; ) の 鍵ですか。", "a": "何", "options": ["何", "誰", "どこ", "どちら"]}
        ]
    },
     {
        "pattern": "Anata no (Yours)",
        "description": "Asking about possession",
        "questions": [
            {"q": "この傘は ( &nbsp;&nbsp; ) のですか。", "a": "あなた", "options": ["あなた", "わたし", "これ", "それ"]},
        ]
    }
]

def generate_vocab_questions(count=30):
    questions = []
    
    # 1. Kanji to Reading
    for _ in range(count // 2):
        item = random.choice(VOCAB)
        correct = item['kana']
        distractors = [x['kana'] for x in random.sample(VOCAB, 3) if x != item]
        options = distractors + [correct]
        random.shuffle(options)
        
        questions.append({
            "type": "vocab_reading",
            "question": f"What is the reading for <span class='text-indigo-600 font-bold'> {item['kanji']} </span>?",
            "options": options,
            "answer": correct,
            "explanation": f"{item['kanji']} reads as {item['kana']} ({item['meaning']})."
        })

    # 2. Reading to Meaning
    for _ in range(count // 2):
        item = random.choice(VOCAB)
        correct = item['meaning']
        distractors = [x['meaning'] for x in random.sample(VOCAB, 3) if x != item]
        options = distractors + [correct]
        random.shuffle(options)
        
        questions.append({
            "type": "vocab_meaning",
            "question": f"What does <span class='text-indigo-600 font-bold'> {item['kana']} </span> mean?",
            "options": options,
            "answer": correct,
            "explanation": f"{item['kana']} means {item['meaning']} ({item['kanji']})."
        })
        
    return questions

def generate_grammar_questions(count=30):
    questions = []
    
    for _ in range(count):
        pattern = random.choice(GRAMMAR_PATTERNS)
        template = random.choice(pattern['questions'])
        
        options = template['options'][:] # Copy
        random.shuffle(options)
        
        questions.append({
            "type": "grammar_particle",
            "question": template['q'],
            "options": options,
            "answer": template['a'],
            "explanation": f"Pattern: {pattern['description']}"
        })
        
    return questions

def generate_context_questions(count=20):
    questions = []
    
    contexts = [
        {
            "q": "A: これはテレホンカードですか。<br>B: いいえ、( &nbsp;&nbsp; )。",
            "a": "違います",
            "options": ["そうです", "違います", "はい", "これです"],
            "expl": "Negative response: 'No, it isn't' (Iie, chigaimasu)."
        },
        {
            "q": "A: それは誰の傘ですか。<br>B: ( &nbsp;&nbsp; ) のです。",
            "a": "私",
            "options": ["私", "これ", "それ", "あれ"],
            "expl": "Possession answer: 'Watashi no desu' (It's mine)."
        },
        {
            "q": "A: この本はあなたのですか。<br>B: いいえ、( &nbsp;&nbsp; ) のではありません。",
            "a": "私",
            "options": ["私", "あなた", "誰", "何"],
            "expl": "Negative interaction."
        },
        {
            "q": "A: ありがとうございます。<br>B: ( &nbsp;&nbsp; )。",
            "a": "いいえ、どういたしまして",
            "options": ["いいえ、どういたしまして", "はい、そうです", "違います", "お願いします"],
            "expl": "Response to Thank you: You're welcome."
        }
    ]
    
    for _ in range(count):
        ctx = random.choice(contexts)
        options = ctx['options'][:]
        random.shuffle(options)
        
        questions.append({
            "type": "context_dialogue",
            "question": ctx['q'],
            "options": options,
            "answer": ctx['a'],
            "explanation": ctx['expl']
        })
        
    return questions

def generate_listening_questions(count=20):
    questions = []
    # Simuluate listening with reading questions for now, or numbers
    
    for i in range(count):
        num = random.randint(1, 100)
        q_text = f"Select the reading for the number: {num}"
        # We need a proper number to japanese functions, but let's stick to basics for this demo or specific list
        # Simply using vocab items as 'Listening' checks (simulated)
        
        item = random.choice(VOCAB)
        correct = item['kanji']
        distractors = [x['kanji'] for x in random.sample(VOCAB, 3) if x != item]
        options = distractors + [correct]
        random.shuffle(options)
        
        questions.append({
            "type": "listening_sim",
            "question": f"🔊 [Audio: {item['kana']}] <br> Choose the correct Kanji:",
            "options": options,
            "answer": correct,
            "explanation": f"Audio said '{item['kana']}', which is {item['kanji']}."
        })
        
    return questions

def main():
    test_data = {
        "vocabulary": generate_vocab_questions(30),
        "grammar": generate_grammar_questions(30),
        "context": generate_context_questions(20),
        "listening": generate_listening_questions(20)
    }
    
    # Wrap in JS variable
    js_content = f"const LESSON2_TEST_DATA = {json.dumps(test_data, ensure_ascii=False, indent=2)};"
    
    with open('lesson2_test_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("Generated lesson2_test_data.js with 100 questions.")

if __name__ == "__main__":
    main()
