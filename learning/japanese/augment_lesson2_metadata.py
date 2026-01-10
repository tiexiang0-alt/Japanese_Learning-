
import os
import re

TARGET_FILE = "chapter2_lesson2.html"

# Data for Missing Sections
# We focus mainly on Origin (词源) as it's most commonly missing.
# We can also backfill Structure (构词) or Memory (记忆) if needed.

# Format: Word -> { 'origin': '...', 'structure': '...', 'memory': '...' }
# Only fields that need injection are critical, but providing all helps.

METADATA_DB = {
    "辞書": {"origin": "汉字词 (Kango)", "structure": "辞 (Words) + 書 (Book)", "memory": "辞書で言葉を調べます。"},
    "雑誌": {"origin": "汉字词 (Kango)", "structure": "雑 (Misc) + 誌 (Record)", "memory": "雑誌は面白いです。"},
    "電話": {"origin": "汉字词 (Kango)", "structure": "電 (Electricity) + 話 (Talk)", "memory": "電話で話します。"},
    "鞄":   {"origin": "汉字词 (Kango)", "structure": "革 (Leather) + 包 (Wrap)", "memory": "鞄に本を入れます。"},
    "鉛筆": {"origin": "汉字词 (Kango)", "structure": "鉛 (Lead) + 筆 (Brush)", "memory": "鉛筆で書きます。"},
    "傘":   {"origin": "和语 (Wago)",   "structure": "象形 (Pictograph)", "memory": "雨の日は傘をさします。"},
    "靴":   {"origin": "和语 (Wago)",   "structure": "革 (Leather) + 化 (Change)", "memory": "新しい靴を履きます。"},
    "新聞": {"origin": "汉字词 (Kango)", "structure": "新 (New) + 聞 (Hear)", "memory": "毎朝新聞を読みます。"},
    "机":   {"origin": "和语 (Wago)",   "structure": "木 (Wood) + 几 (Desk)", "memory": "机の上を片付けます。"},
    "椅子": {"origin": "汉字词 (Kango)", "structure": "木 (Wood) + 奇 (Strange?)", "memory": "椅子に座ります。"}, # Simplified
    "鍵":   {"origin": "和语 (Wago)",   "structure": "金 (Metal) + 建 (Build)", "memory": "鍵を閉めます。"},
    "時計": {"origin": "汉字词 (Kango)", "structure": "時 (Time) + 計 (Measure)", "memory": "時計を見ます。"},
    "手帳": {"origin": "汉字词 (Kango)", "structure": "手 (Hand) + 帳 (Curtain/Book)", "memory": "手帳に予定を書きます。"},
    "写真": {"origin": "汉字词 (Kango)", "structure": "写 (Copy) + 真 (Truth)", "memory": "写真を撮りましょう。"},
    "車":   {"origin": "和语 (Wago)",   "structure": "象形 (Pictograph)", "memory": "車を運転します。"},
    "自転車": {"origin": "汉字词 (Kango)", "structure": "自(Self)+転(Turn)+車(Car)", "memory": "自転車で学校へ行きます。"},
    "お土産": {"origin": "和语 (Wago)",   "structure": "土 (Earth) + 産 (Product)", "memory": "お土産を買いました。"},
    "名産品": {"origin": "汉字词 (Kango)", "structure": "名(Name)+産(Product)+品(Item)", "memory": "これは名産品です。"},
    "パソコン": {"origin": "外来语 (Gairaigo)", "structure": "Personal Computer", "memory": "パソコンを使います。"},
    "カメラ":   {"origin": "外来语 (Gairaigo)", "structure": "Camera", "memory": "カメラが好きです。"},
    "テレビ":   {"origin": "外来语 (Gairaigo)", "structure": "Television", "memory": "テレビを見ます。"},
    "ニュース": {"origin": "外来语 (Gairaigo)", "structure": "News", "memory": "ニュースを聞きます。"},
    "家族": {"origin": "汉字词 (Kango)", "structure": "家 (House) + 族 (Tribe)", "memory": "家族を大切にします。"},
    "母":   {"origin": "和语 (Wago)",   "structure": "象形 (Pictograph)", "memory": "母に電話します。"},
    "方":   {"origin": "和语 (Wago)",   "structure": "象形 (Direction/Person)", "memory": "あの方は先生です。"},
    "人":   {"origin": "和语 (Wago)",   "structure": "象形 (Person)", "memory": "あの人は誰ですか。"},
    "会社": {"origin": "汉字词 (Kango)", "structure": "会 (Meet) + 社 (Shrine/Company)", "memory": "会社へ行きます。"},
    "シルク": {"origin": "外来语 (Gairaigo)", "structure": "Silk", "memory": "シルクは柔らかいです。"},
    "ハンカチ": {"origin": "外来语 (Gairaigo)", "structure": "Handkerchief", "memory": "ハンカチを持ちます。"},
    "日本語": {"origin": "汉字词 (Kango)", "structure": "日(Sun)+本(Origin)+語(Lang)", "memory": "日本語を勉強します。"},
    "教科書": {"origin": "汉字词 (Kango)", "structure": "教(Teach)+科(Subj)+書(Book)", "memory": "教科書を読みます。"},
    "手紙":   {"origin": "汉字词 (Kango)", "structure": "手 (Hand) + 紙 (Paper)", "memory": "手紙を書きます。"},
    "会社員": {"origin": "汉字词 (Kango)", "structure": "会社(Company)+員(Member)", "memory": "会社員になります。"},
    "お母さん": {"origin": "和语 (Wago)",   "structure": "お(Hon)+母(Mother)+さん", "memory": "お母さんは優しいです。"},
    "ノート": {"origin": "外来语 (Gairaigo)", "structure": "Note (book)", "memory": "ノートに書きます。"},
    "ボールペン": {"origin": "外来语 (Gairaigo)", "structure": "Ball + Pen", "memory": "ボールペンを買います。"},
    "シャープペンシル": {"origin": "和制英语 (Wasei)", "structure": "Sharp + Pencil", "memory": "シャープペンシルを使います。"},
    "自動車": {"origin": "汉字词 (Kango)", "structure": "自(Self)+動(Move)+車(Car)", "memory": "自動車を運転します。"},
    "プレゼント": {"origin": "外来语 (Gairaigo)", "structure": "Present", "memory": "プレゼントをあげます。"},
    "バッグ": {"origin": "外来语 (Gairaigo)", "structure": "Bag", "memory": "バッグを持ちます。"},
    "靴下": {"origin": "和语 (Wago)", "structure": "靴 (Shoe) + 下 (Under)", "memory": "靴下を履きます。"},
    "ケータイ": {"origin": "外来语 (Gairaigo)", "structure": "Mobile (Keitai)", "memory": "ケータイを使います。"},
    "テーブル": {"origin": "外来语 (Gairaigo)", "structure": "Table", "memory": "テーブルで食事します。"},
    "腕時計": {"origin": "汉字词 (Kango)", "structure": "腕(Wrist)+時(Time)+計(Meter)", "memory": "腕時計を見ます。"},
    "漫画": {"origin": "汉字词 (Kango)", "structure": "漫(Random)+画(Picture)", "memory": "漫画を読みます。"},
}

def create_section_html(title, color_class, content):
    # Standard template for a metadata row
    # To match: <div class="flex items-start gap-2 text-xs"> ... </div>
    return f"""
                            <div class="flex items-start gap-2 text-xs">
                                <span class="font-bold {color_class} w-8 shrink-0">{title}</span>
                                <span class="text-slate-600">{content}</span>
                            </div>"""

def process_file():
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strategy:
    # Iterate through all known words.
    # Find their card in HTML.
    # Check for presence of Component, Origin, Memory, Usage.
    # Inject missing ones in correct order.
    
    # Priority Order in HTML:
    # 1. Structure (构词) - text-slate-400
    # 2. Origin (词源) - text-slate-400 (or maybe blue/indigo if distinct?) Let's use text-slate-400 or text-indigo-400? 
    #    Existing 'Book' used `text-slate-400` for Origin too? Let's verify layout.
    # 3. Memory (记忆) - text-amber-500
    # 4. Usage (用法) - text-emerald-500
    
    for vocab, data in METADATA_DB.items():
        # strict regex for title to avoid partial matches
        # <span class="text-[23]xl font-bold text-slate-800">vocab</span>
        # Support xl, 2xl, 3xl, 4xl
        vocab_pattern = f'<span class="text-[1-4]?xl font-bold text-slate-800">{vocab}</span>'
        match = re.search(vocab_pattern, content)
        
        if not match:
            print(f"Skipping {vocab} - Not found in HTML.")
            continue
            
        start_idx = match.start()
        # Find the metadata container div. It's usually `class="mt-4 pt-3 border-t ..."` or `mt-2 pt-2`
        # We can search forward for `border-t border-slate-200/50`
        
        container_match = re.search(r'class="mt-[24] pt-[23] border-t border-slate-200/50 space-y-[12]">', content[start_idx:])
        
        if not container_match:
            print(f"Warning: Metadata container not found for {vocab}")
            continue
            
        container_start_abs = start_idx + container_match.end()
        
        # We need to find the END of this container. usually `</div> \n </div>`?
        # Or just operate inside the block.
        # Let's extract the block until the next `glass-panel` or significant tag?
        # Easier: Extract next 1000 chars and find the closing </div> of the container.
        # The container opens a div, so we look for matching closing div.
        # But scanning is safer if we look for the *next* known element or card closure.
        
        # Determine current sections
        # We check specific strings to see if they exist in the vicinity (next 500 chars)
        search_region_len = 800
        search_region = content[container_start_abs:container_start_abs+search_region_len]
        
        if vocab == "シャープペンシル":
            print(f"DEBUG: Found {vocab} at {start_idx}")
            print(f"DEBUG: Container starts at {container_start_abs}")
            print(f"DEBUG: Has Origin: {'词源' in search_region}")
            print(f"DEBUG: Has Structure: {'构词' in search_region}")
        
        has_structure = '构词' in search_region
        has_origin = '词源' in search_region
        has_memory = '记忆' in search_region
        has_usage = '用法' in search_region
        
        # Injection logic
        # We want order: Structure -> Origin -> Memory -> Usage
        
        # 1. Check Structure
        if not has_structure and 'structure' in data:
            html = create_section_html("构词", "text-slate-400", data['structure'])
            # Insert at beginning of container
            content = content[:container_start_abs] + html + content[container_start_abs:]
            print(f"Injected Structure for {vocab}")
            has_structure = True # Mark as present for next steps relative positioning?
            # Adjust offsets?
            # Actually, if we modify `content`, our indices `container_start_abs` become invalid for *subsequent* operations on THIS word?
            # Yes. So we should re-read or offset?
            # Or simpler: build the inner HTML and replace the Whole Container inner part?
            # No, replacing whole container is risky if we lose existing Usage buttons etc.
            
            # Let's recalculate container_start_abs since we just shifted it? 
            # No, if we insert AT `container_start_abs`, the "rest" shifts right.
            # So `container_start_abs` is still the insertion point for *subsequent* items if we want them *after* this new one?
            # Wait. If I insert Structure at Start, fine.
            # Next I want to insert Origin. It should go *after* Structure.
            
            # Re-eval strategy:
            # We assume we are doing one pass per word.
            # Just accumulate valid HTML chunks?
            
            pass 
            # Doing sequential string modification is tricky with indices.
            # Let's use the replacement approach on the unique string match of the container opening?
            # Too generic.
        
    # Better Strategy:
    # 1. Split content by Cards? No.
    # 2. Iterate and rebuild?
    # 3. Just use correct relative insertions.
    
    # Let's try to inject missing fields ONE BY ONE per word, updating `content` variable.
    # But we need to re-find the word location each time or track offset.
    
    # We can iterate words. For each word:
    #   Find location.
    #   Check structure -> Inject if missing. Update content.
    #   Find location (it shifted).
    #   Check Origin -> Inject if missing. Update content.
    #   ...
    
    words_processed = 0
    
    for vocab, data in METADATA_DB.items():
        # We loop through sections
        sections = [
            ("structure", "构词", "text-slate-400", None), # None means insert at start (default) or before next
            ("origin",    "词源", "text-slate-400", "构词"), # Insert after Structure
            ("memory",    "记忆", "text-amber-500", "词源"), # Insert after Origin
            ("usage",     "用法", "text-emerald-500", "记忆") # Insert after Memory
        ]
        
        # But wait, Usage handles its own specialized HTML (audio button), so we might skip injecting Usage if missing effectively?
        # The prompt says "supplement complete".
        # If Usage is missing, we use our `process_lesson2_usage.py`? 
        # Actually `process_lesson2_usage.py` handles Usage injection well.
        # This script should focus on Structure, Origin, Memory since Usage is complex.
        # But let's check Usage existence just in case. If missing, we warn or inject placeholder?
        # Let's assume Usage is handled by other script, focus on Structure/Origin/Memory.
        
        target_sections = ["structure", "origin", "memory"] 
        
        for key in target_sections:
            if key not in data: continue
            
            # Re-Find word in current content
            vocab_pattern = f'<span class="text-[1-4]?xl font-bold text-slate-800">{vocab}</span>'
            match = re.search(vocab_pattern, content)
            if not match: break
            
            start_idx = match.start()
            container_match = re.search(r'class="mt-[24] pt-[23] border-t border-slate-200/50 space-y-[12]">', content[start_idx:])
            if not container_match: break
            
            container_start = start_idx + container_match.end()
            search_window = content[container_start : container_start + 1000]
            
            # Define tags
            title_map = {"structure": "构词", "origin": "词源", "memory": "记忆"}
            title = title_map[key]
            
            if f'>{title}</span>' in search_window:
                continue # Already exists
            
            # Make HTML
            color_map = {"structure": "text-slate-400", "origin": "text-slate-400", "memory": "text-amber-500"}
            html = create_section_html(title, color_map[key], data[key])
            
            # Determine Insertion Point
            # If Structure: Insert at start of container.
            # If Origin: Insert after Structure (if exists) or at start.
            # If Memory: Insert after Origin (if exists) or Structure (if exists) or at start.
            
            insert_pos = container_start
            
            if key == "structure":
                insert_pos = container_start
            
            elif key == "origin":
                # Find Structure closing div?
                # Look for `构词` and its closing `</div>`
                struct_match = re.search(r'构词</span>.*?</div>', search_window, re.DOTALL)
                if struct_match:
                    insert_pos = container_start + struct_match.end()
                else:
                    insert_pos = container_start
                    
            elif key == "memory":
                 # Find Origin OR Structure
                 origin_match = re.search(r'词源</span>.*?</div>', search_window, re.DOTALL)
                 if origin_match:
                     insert_pos = container_start + origin_match.end()
                 else:
                     struct_match = re.search(r'构词</span>.*?</div>', search_window, re.DOTALL)
                     if struct_match:
                         insert_pos = container_start + struct_match.end()
                     else:
                         insert_pos = container_start
            
            # Inject
            content = content[:insert_pos] + html + content[insert_pos:]
            print(f"Injected {key} for {vocab}")
            words_processed += 1

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Total injections: {words_processed}")

if __name__ == "__main__":
    process_file()
