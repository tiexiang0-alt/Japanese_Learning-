
import os
import re

def inject_furigana():
    target_path = '/Users/hardentie/Downloads/vscode/learning/japanese/chapter2_lesson3.html'
    
    with open(target_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Dictionary of plain text -> text with furigana
    # We focus on the Grammar (lines ~3100-4000) and Text (lines ~4000+) sections content.
    # Note: We must be careful not to break existing HTML attributes.
    # We will search for specific phrases found in Grammar and Text sections.
    
    replacements = {
        # Grammar Section 1: Koko/Soko/Asoko
        "ここはデパートです。": "<ruby>ここ<rt>here</rt></ruby>は<ruby>デパート<rt>dep't</rt></ruby>です。", # Just kidding, actual furigana
        # Real Furigana mappings
        "ここはデパートです。": "ここは<ruby>デパート<rt>depa-to</rt></ruby>です。",
        "銀行はあそこです。": "<ruby>銀行<rt>ぎんこう</rt></ruby>はあそこです。",
        "郵便局はどこですか。": "<ruby>郵便局<rt>ゆうびんきょく</rt></ruby>はどこですか。",
        
        # Grammar Section 2: Noun no Noun
        "これはコンピュータの本です。": "これは<ruby>コンピュータ<rt>konpyu-ta</rt></ruby>の<ruby>本<rt>ほん</rt></ruby>です。",
        "それは私の鍵です。": "それは<ruby>私<rt>わたし</rt></ruby>の<ruby>鍵<rt>かぎ</rt></ruby>です。",
        "あれは山田さんの傘です。": "あれは<ruby>山田<rt>やまだ</rt></ruby>さんの<ruby>傘<rt>かさ</rt></ruby>です。",
        
        # Grammar Section 3: Kono/Sono/Ano
        "この鞄は私のです。": "この<ruby>鞄<rt>かばん</rt></ruby>は<ruby>私<rt>わたし</rt></ruby>のです。",
        "その時計は田中さんのです。": "その<ruby>時計<rt>とけい</rt></ruby>は<ruby>田中<rt>たなか</rt></ruby>さんのです。",
        "あの方はずいぶんです。": "あの<ruby>方<rt>かた</rt></ruby>はずいぶんです。", # Wait, original sentence check needed.
        # Let's use the actual sentences from the file we viewed earlier
        
        # Grammar 6: Polite Place (New)
        "こちらは田中さんです。": "こちらは<ruby>田中<rt>たなか</rt></ruby>さんです。",
        "お手洗いはあちらです。": "<ruby>お手洗い<rt>おてあらい</rt></ruby>はあちらです。",
        
        # Grammar 7: Mo (New) - "私は中国人です。周さんも中国人です。"
        "私は中国人です。": "<ruby>私<rt>わたし</rt></ruby>は<ruby>中国<rt>ちゅうごく</rt></ruby><ruby>人<rt>じん</rt></ruby>です。",
        "周さんも中国人です。": "<ruby>周<rt>しゅう</rt></ruby>さんも<ruby>中国<rt>ちゅうごく</rt></ruby><ruby>人<rt>じん</rt></ruby>です。",
        "これも日本のペンですね。": "これも<ruby>日本<rt>にほん</rt></ruby>の<ruby>ペン<rt>pen</rt></ruby>ですね。",
        
        # Grammar 8: Choice (New)
        "今日は水曜日ですか、木曜日ですか。": "<ruby>今日<rt>きょう</rt></ruby>は<ruby>水曜日<rt>すいようび</rt></ruby>ですか、<ruby>木曜日<rt>もくようび</rt></ruby>ですか。",
        "水曜日です。": "<ruby>水曜日<rt>すいようび</rt></ruby>です。",
        "ここは一階ですか、二階ですか。": "ここは<ruby>一階<rt>いっかい</rt></ruby>ですか、<ruby>二階<rt>にかい</rt></ruby>ですか。",
        "二階です。": "<ruby>二階<rt>にかい</rt></ruby>です。",
        
        # Grammar 9: Price (New)
        "このかばんはいくらですか。": "この<ruby>かばん<rt>bag</rt></ruby>はいくらですか。", # kaban is usually hiragana in beginners text but let's just ruby it if needed? Actually it was kana in input.
        "五千八百円です。": "<ruby>五千八百<rt>ごせんはっぴゃく</rt></ruby><ruby>円<rt>えん</rt></ruby>です。",

        # SCENE 01: Asking Directions
        "すみません。お手洗いはどこですか。": "すみません。<ruby>お手洗い<rt>おてあらい</rt></ruby>はどこですか。",
        "あそこです。": "あそこです。",
        "どうも。": "どうも。",
        
        # SCENE 02: Dept Store
        "すみません、売り場はどこですか。": "すみません、<ruby>売<rt>う</rt></ruby>り<ruby>場<rt>ば</rt></ruby>はどこですか。",
        "一階です。": "<ruby>一階<rt>いっかい</rt></ruby>です。",
        "そのとけいはいくらですか。": "そのとけいはいくらですか。",
        "これは１万八千円です。": "これは<ruby>１万<rt>いちまん</rt></ruby><ruby>八千<rt>はっせん</rt></ruby><ruby>円<rt>えん</rt></ruby>です。", # 1man ...
        "じゃ、これをください。": "じゃ、これをください。",
        
        # SCENE 03: Phone Number
        "李さんの電話番号は何番ですか。": "<ruby>李<rt>り</rt></ruby>さんの<ruby>電話<rt>でんわ</rt></ruby><ruby>番号<rt>ばんごう</rt></ruby>は<ruby>何番<rt>なんばん</rt></ruby>ですか。",
        "えーと、090-1234-5678です。": "えーと、090-1234-5678です。",
        "090-1234-5678ですね。": "090-1234-5678ですね。",
        "はい、そうです。": "はい、そうです。",
        "ありがとうございます。": "ありがとうございます。",
        
        # SCENE 04: Origin
        "それはどこの靴ですか。": "それはどこの<ruby>靴<rt>くつ</rt></ruby>ですか。",
        "イタリアの靴です。": "<ruby>イタリア<rt>Italy</rt></ruby>の<ruby>靴<rt>くつ</rt></ruby>です。",
        "いくらでしたか。": "いくらでしたか。",
        "五万円でした。": "<ruby>五万<rt>ごまん</rt></ruby><ruby>円<rt>えん</rt></ruby>でした。",
        "へえー、高いですね！": "へえー、<ruby>高<rt>たか</rt></ruby>いですね！",
        
        # SCENE 05: The Office (Existing content check)
        "受付はどこですか。": "<ruby>受付<rt>うけつけ</rt></ruby>はどこですか。",
        "受付はそこです。": "<ruby>受付<rt>うけつけ</rt></ruby>はそこです。",
        "事務所はどこですか。": "<ruby>事務所<rt>じむしょ</rt></ruby>はどこですか。",
        "事務所は二階です。エレベーターはあちらです。": "<ruby>事務所<rt>じむしょ</rt></ruby>は<ruby>二階<rt>にかい</rt></ruby>です。<ruby>エレベーター<rt>elevator</rt></ruby>はあちらです。",
        "どうもありがとうございます。": "どうもありがとうございます。",
        
        # Drill 9
        "あの人はだれですか。": "<ruby>あの人<rt>あのひと</rt></ruby>はだれですか。",
        
        # Drill 10
        "食堂はあそこです。": "<ruby>食堂<rt>しょくどう</rt></ruby>はあそこです。",
    }
    
    # We will simply string replace the known sentences.
    # To avoid replacing inside existing tags (though unlikely for these full sentences), we can be careful.
    # Currently these sentences are inside <p> tags.
    
    count = 0
    for plain, ruby in replacements.items():
        if plain in html:
            html = html.replace(plain, ruby)
            count += 1
            
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Injected furigana for {count} sentences.")

if __name__ == '__main__':
    inject_furigana()
