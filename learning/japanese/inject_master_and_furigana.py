
import os
import re

def inject_and_annotate():
    base_dir = '/Users/hardentie/Downloads/vscode/learning/japanese'
    target_path = os.path.join(base_dir, 'chapter2_lesson3.html')
    master_html_path = os.path.join(base_dir, 'lesson3_master_scene.html')
    
    with open(master_html_path, 'r', encoding='utf-8') as f:
        master_html = f.read()
        
    with open(target_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Clean up existing Master Scene if present
    # We look for the start and end of the Master Dialogue block.
    # It starts with `<!-- Master Scene -->` and ends at the closing `</div>` of the container.
    # Or we can identify it by ID if we added one (we added id="master-dialogue-container" in the new script).
    # But the OLD hidden one didn't have ID. It had `<!-- Master Scene -->`.
    
    start_marker = '<!-- Master Scene -->'
    
    if start_marker in html:
        print("Existing Master Scene found. Removing it...")
        # Since we inserted it before `<!-- 4. Culture Section -->` and it ends with a div.
        # Let's find the Culture Section marker.
        culture_marker = '<!-- 4. Culture Section -->'
        
        # We assume the Master Scene is immediately before the Culture Section (with some newlines/divs).
        # We can regex replace the block from `<!-- Master Scene -->` up to `<!-- 4. Culture Section -->`
        # BUT we need to keep the closing divs of the Text Section that were there before?
        # In the previous injection, I inserted `master_html` inside the text section content.
        # `new_pre = pre_culture[:idx] + '\n' + master_html + '\n' + pre_culture[idx:]`
        # So Master Scene is wrapped by Text Section divs?
        # Wait, `pre_culture[:idx]` splits at the last `</div>`.
        # So Master Scene is INSIDE the last div? No, before the last closing div.
        # So it is INSIDE `#content-text`.
        
        # Safe strategy:
        # Regex replace `<!-- Master Scene -->[\s\S]*?<!-- 4. Culture Section -->` is too aggressive if there are closing divs in between.
        # Let's locate `<!-- Master Scene -->` and the next `<!-- 4. Culture Section -->`.
        # Split by Start Marker.
        
        parts = html.split(start_marker)
        if len(parts) > 1:
            pre_master = parts[0]
            # The part after looks like: `... HTML content ... </div></div> <!-- 4. Culture Section --> ...`
            # We want to remove everything up to the END of Master Scene.
            # Master Scene ends with `</div>` (footer).
            
            # Since we are re-injecting, let's just strip the old one out if we can find its boundary.
            # The new HTML has `id="master-dialogue-container"`. The old one key phrase: `综合演练 (Master Dialogue)`
            
            # SIMPLER APPROACH:
            # Revert to a clean state if possible? No backup.
            # Let's just remove the block if we can identify it.
            # The block starts with `<!-- Master Scene -->` and ends before `<!-- 4. Culture Section -->` BUT after some `</div>`s?
            # Actually, in Step 2747 injection:
            # `new_pre = pre_culture[:idx] + '\n' + master_html + '\n' + pre_culture[idx:]`
            # It was inserted before the last closing div of the text section.
            
            # So the structure is:
            # ... old text content ...
            # <!-- Master Scene -->
            # ... master content ...
            # </div> (end of master container)
            # </div> (end of #content-text)
            # <!-- 4. Culture Section -->
            
            # So, if we search for `<!-- Master Scene -->` ... `</div>` ... `</div>` ... `Culture`.
            # We can replace `<!-- Master Scene -->.*?(?=</div>\s*</div>\s*<!-- 4. Culture Section -->)`?
            # Regex is tricky with nested divs.
            
            # Let's use string manipulation.
            # Find `<!-- Master Scene -->`.
            # Find `<!-- 4. Culture Section -->`.
            # The content between them is the Master Scene HTML + closing div of #content-text.
            # Wait, `pre_culture[idx:]` was `</div>\n\n`.
            # So we inserted Master Scene BEFORE the last div.
            # So effectively: `<!-- Master Scene --> ... </div>` is followed by `</div>` (Text End).
            
            # To delete: Remove from `<!-- Master Scene -->` up to the character before the last `</div>`.
            # How to find the last `</div>` before Culture Section?
            # It is the one we used for injection.
            
            culture_pos = html.find(culture_marker)
            if culture_pos != -1:
                # Look backwards from Culture Section for `</div>`.
                # This is the Text Section closer.
                text_end_div_pos = html.rfind('</div>', 0, culture_pos)
                
                # Verify Master Scene Start is before this.
                master_start_pos = html.find(start_marker, 0, text_end_div_pos)
                
                if master_start_pos != -1:
                     # Remove everything from master_start_pos to text_end_div_pos
                     # But check if there is whitespace.
                     html = html[:master_start_pos] + html[text_end_div_pos:]
                     print("Removed old Master Scene.")
    
    # 2. Injection (Fresh)
    marker_culture = '<!-- 4. Culture Section -->'
    if marker_culture in html:
        parts = html.split(marker_culture)
        pre_culture = parts[0]
        post_culture = parts[1]
        
        idx = pre_culture.rfind('</div>')
        if idx != -1:
            new_pre = pre_culture[:idx] + '\n' + master_html + '\n' + pre_culture[idx:]
            html = new_pre + marker_culture + post_culture
            print("Successfully injected Expanded Master Scene HTML.")
        else:
            print("Error: Could not find closing div for Text section.")
            return
    else:
        print("Error: Culture Section marker not found.")
        return

    # 3. Furigana Annotation (Part 1 & 2 sentences)
    replacements = {
        # Part 1
        "すみません、ネクタイ売り場はどこですか。": "すみません、<ruby>ネクタイ<rt>necktie</rt></ruby><ruby>売<rt>う</rt></ruby>り<ruby>場<rt>ば</rt></ruby>はどこですか。",
        "三階です。エスカレーターはあちらです。": "<ruby>三階<rt>さんがい</rt></ruby>です。<ruby>エスカレーター<rt>escalator</rt></ruby>はあちらです。",
        "どうもありがとうございます。": "どうもありがとうございます。",
        "すみません、これはどこのネクタイですか。": "すみません、これはどこの<ruby>ネクタイ<rt>necktie</rt></ruby>ですか。",
        "それはイタリアのネクタイです。": "それは<ruby>イタリア<rt>Italy</rt></ruby>の<ruby>ネクタイ<rt>necktie</rt></ruby>です。",
        "いくらですか。": "いくらですか。",
        "一万五千円です。": "<ruby>一万<rt>いちまん</rt></ruby><ruby>五千<rt>ごせん</rt></ruby><ruby>円<rt>えん</rt></ruby>です。",
        "ちょっと高いですね。じゃ、あれは？": "ちょっと<ruby>高<rt>たか</rt></ruby>いですね。じゃ、あれは？",
        "あれは日本のネクタイです。五千八百円です。": "あれは<ruby>日本<rt>にほん</rt></ruby>の<ruby>ネクタイ<rt>necktie</rt></ruby>です。<ruby>五千八百<rt>ごせんはっぴゃく</rt></ruby><ruby>円<rt>えん</rt></ruby>です。",
        "そうですか。じゃ、あれをください。": "そうですか。じゃ、あれをください。",
        "このハンカチもください。": "この<ruby>ハンカチ<rt>handkerchief</rt></ruby>もください。",
        "はい。全部で七千円です。": "はい。<ruby>全部<rt>ぜんぶ</rt></ruby>で<ruby>七千<rt>ななせん</rt></ruby><ruby>円<rt>えん</rt></ruby>です。",
        
        # Part 2 (New)
        "ここは静かですね。": "ここは<ruby>静<rt>しず</rt></ruby>かですね。",
        "ええ。この周辺はとても便利です。": "ええ。この<ruby>周辺<rt>しゅうへん</rt></ruby>はとても<ruby>便利<rt>べんり</rt></ruby>です。",
        "あの建物はホテルですか。": "あの<ruby>建物<rt>たてもの</rt></ruby>は<ruby>ホテル<rt>hotel</rt></ruby>ですか。",
        "いいえ、あれはマンションです。ホテルは隣です。": "いいえ、あれは<ruby>マンション<rt>mansion</rt></ruby>です。<ruby>ホテル<rt>hotel</rt></ruby>は<ruby>隣<rt>となり</rt></ruby>です。",
        "郵便局はどこですか。": "<ruby>郵便局<rt>ゆうびんきょく</rt></ruby>はどこですか。",
        "郵便局はあそこです。銀行の隣です。": "<ruby>郵便局<rt>ゆうびんきょく</rt></ruby>はあそこです。<ruby>銀行<rt>ぎんこう</rt></ruby>の<ruby>隣<rt>となり</rt></ruby>です。",
        "図書館もありますか。": "<ruby>図書館<rt>としょかん</rt></ruby>もありますか。",
        "ええ。でも、今日は水曜日ですね。休みです。": "ええ。でも、<ruby>今日<rt>きょう</rt></ruby>は<ruby>水曜日<rt>すいようび</rt></ruby>ですね。<ruby>休<rt>やす</rt></ruby>みです。",
        "そうですか。事務所は何階ですか。": "そうですか。<ruby>事務所<rt>じむしょ</rt></ruby>は<ruby>何階<rt>なんかい</rt></ruby>ですか。",
        "事務所は二階です。受付はこちらです。": "<ruby>事務所<rt>じむしょ</rt></ruby>は<ruby>二階<rt>にかい</rt></ruby>です。<ruby>受付<rt>うけつけ</rt></ruby>はこちらです。",
        "食堂はどこですか。": "<ruby>食堂<rt>しょくどう</rt></ruby>はどこですか。",
        "食堂は地下です。安いです。": "<ruby>食堂<rt>しょくどう</rt></ruby>は<ruby>地下<rt>ちか</rt></ruby>です。<ruby>安<rt>やす</rt></ruby>いです。",
    }
    
    count = 0
    for plain, ruby in replacements.items():
        if plain in html:
            html = html.replace(plain, ruby)
            count += 1
            
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Applied furigana to {count} master scene sentences.")

if __name__ == '__main__':
    inject_and_annotate()
