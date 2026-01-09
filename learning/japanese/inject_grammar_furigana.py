
import os

def inject_grammar_furigana():
    base_dir = '/Users/hardentie/Downloads/vscode/learning/japanese'
    target_path = os.path.join(base_dir, 'chapter2_lesson3.html')
    
    with open(target_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Mappings for Grammar Section Sentences
    replacements = {
        # Pattern 1
        "ここは教室です。": "ここは<ruby>教室<rt>きょうしつ</rt></ruby>です。",
        "そこは受付です。": "そこは<ruby>受付<rt>うけつけ</rt></ruby>です。",
        "あそこはロビーです。": "あそこはロビーです。", # No Kanji, but keeping for completeness if needed? No change.
        "ここは食堂ではありません。": "ここは<ruby>食堂<rt>しょくどう</rt></ruby>ではありません。",
        "そこは事務所ですか。": "そこは<ruby>事務所<rt>じむしょ</rt></ruby>ですか。",
        
        # Pattern 2
        "お手洗いはどこですか。": "お<ruby>手洗<rt>てあら</rt></ruby>いはどこですか。",
        "電話はどこですか。": "<ruby>電話<rt>でんわ</rt></ruby>はどこですか。",
        "京藤先生はどこですか。": "<ruby>京藤<rt>きょうとう</rt></ruby><ruby>先生<rt>せんせい</rt></ruby>はどこですか。",
        "エレベーターはどちらですか。": "エレベーターはどちらですか。",
        "会議室はどちらですか。": "<ruby>会議室<rt>かいぎしつ</rt></ruby>はどちらですか。",
        
        # Pattern 3
        "食堂は一階です。": "<ruby>食堂<rt>しょくどう</rt></ruby>は<ruby>一階<rt>いっかい</rt></ruby>です。",
        "トイレはあそこです。": "トイレはあそこです。",
        "事務所は二階です。": "<ruby>事務所<rt>じむしょ</rt></ruby>は<ruby>二階<rt>にかい</rt></ruby>です。",
        "ロビーはここです。": "ロビーはここです。",
        "靴売り場は一階です。": "<ruby>靴<rt>くつ</rt></ruby><ruby>売<rt>う</rt></ruby>り<ruby>場<rt>ば</rt></ruby>は<ruby>一階<rt>いっかい</rt></ruby>です。",
        
        # Pattern 4
        "これはいくらですか。": "これはいくらですか。",
        "そのネクタイはいくらですか。": "そのネクタイはいくらですか。",
        "このワインはいくらですか。": "このワインはいくらですか。",
        "それは三千円です。": "それは<ruby>三千<rt>さんぜん</rt></ruby><ruby>円<rt>えん</rt></ruby>です。",
        "あれは一万五千円です。": "あれは<ruby>一万<rt>いちまん</rt></ruby><ruby>五千<rt>ごせん</rt></ruby><ruby>円<rt>えん</rt></ruby>です。",
        
        # Pattern 5
        "これは日本の車です。": "これは<ruby>日本<rt>にほん</rt></ruby>の<ruby>車<rt>くるま</rt></ruby>です。",
        "それはアメリカのワインですか。": "それはアメリカのワインですか。",
        "あれはどこの靴ですか。": "あれはどこの<ruby>靴<rt>くつ</rt></ruby>ですか。",
        "これはイタリアのネクタイです。": "これはイタリアのネクタイです。",
        "それは中国の電話です。": "それは<ruby>中国<rt>ちゅうごく</rt></ruby>の<ruby>電話<rt>でんわ</rt></ruby>です。",
    }
    
    count = 0
    for plain, ruby in replacements.items():
        # Only replace if the plain text exists AND it hasn't been replaced yet (check for <ruby> in target?)
        # A simple replace works because plain doesn't have tags.
        # But wait, if I run this multiple times?
        # "ここは<ruby>..." won't match "ここは教室..." so it's safe.
        # But we should ensure we target the plain version.
        
        if plain in html:
            html = html.replace(plain, ruby)
            count += 1
            
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Applied furigana to {count} grammar sentences.")

if __name__ == '__main__':
    inject_grammar_furigana()
