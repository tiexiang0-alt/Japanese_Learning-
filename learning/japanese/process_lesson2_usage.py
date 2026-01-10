
import os
import re
import asyncio
import edge_tts

# Configuration
LESSON_HTML = "chapter2_lesson2.html"
AUDIO_OUTPUT_DIR = "assets/audio/lesson2"
VOICE = "ja-JP-NanamiNeural"  # Female voice

# Usage Sentences Data (Vocab -> Sentence)
USAGE_DATA = {
    "本": "これは本です。",
    "鞄": "それは鞄です。",
    "鉛筆": "これは私の鉛筆です。",
    "傘": "あれは誰の傘ですか。",
    "靴": "この靴はいくらですか。",
    "新聞": "新聞を読みます。", # Simple generic
    "パソコン": "これは新しいパソコンです。",
    "カメラ": "このカメラは高いです。",
    "テレビ": "テレビを見ます。",
    "ニュース": "ニュースを聞きます。",
    "机": "机の上に本があります。",
    "椅子": "椅子に座ってください。",
    "鍵": "鍵を失くしました。", # Lost key
    "時計": "この時計はおしゃれです。", # Stylish
    "手帳": "手帳に書きます。",
    "写真": "写真を撮ります。",
    "車": "車で行きます。",
    "自転車": "自転車に乗ります。",
    "お土産": "お土産を買いました。",
    "名産品": "これは地元の名産品です。",
    "辞書": "これは私の辞書です。",
    "雑誌": "雑誌を読みます。",
    "電話": "電話をかけます。",
    "家族": "家族は3人です。",
    "母": "母は元気です。",
    "方": "この方はどなたですか。",
    "人": "あの人は誰ですか。",
    "会社": "会社で働きます。",
    "シルク": "シルクのハンカチです。",
    "ハンカチ": "ハンカチを使います。",
    "教科書": "トムさんの教科書です。",
    "手紙": "日本から手紙が来ました。",
    "会社員": "田中さんは会社員です。",
    "お母さん": "お母さんによろしく。",
    "ノート": "ノートを貸してください。",
    "ボールペン": "黒いボールペンです。",
    "シャープペンシル": "それはシャープペンシルですね。",
    "自動車": "自動車を運転します。",
    "プレゼント": "これは母へのプレゼントです。",
    "バッグ": "そのバッグは素敵ですね。",
    "靴下": "靴下を履きます。",
    "ケータイ": "ケータイでメールします。",
    "テーブル": "テーブルを片付けます。",
    "腕時計": "腕時計をしています。",
    "漫画": "漫画を読みます。",
}

# Ensure audio directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), AUDIO_OUTPUT_DIR), exist_ok=True)

def extract_japanese(text):
    # Remove <rt>...</rt> tags AND their content (the reading)
    clean_text = re.sub(r'<rt>.*?</rt>', '', text)
    # Remove remaining HTML tags (e.g. <ruby>, <span>)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    return clean_text.strip()

async def generate_audio(text, filename):
    output_path = os.path.join(os.path.dirname(__file__), AUDIO_OUTPUT_DIR, filename)
    print(f"Generating: {filename} from '{text}'")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

async def main():
    target_file = os.path.join(os.path.dirname(__file__), LESSON_HTML)
    
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks = []
    
    # Iterate through USAGE_DATA to inject and generate
    for vocab, sentence in USAGE_DATA.items():
        # 1. Find the Vocab Card
        # Pattern: <span class="text-3xl font-bold text-slate-800">本</span>
        # We need to find the "5 Components" section for this vocab item.
        
        # Regex to find the whole card or at least the components section...
        # Support text-3xl or text-2xl
        vocab_pattern = f'<span class="text-[1-4]?xl font-bold text-slate-800">{vocab}</span>'
        vocab_match = re.search(vocab_pattern, content)
        
        if not vocab_match:
            print(f"Warning: Vocab '{vocab}' not found in HTML.")
            continue
            
        vocab_idx = vocab_match.start()
            
        # Extract a chunk of text after the title to work with (e.g., next 2000 chars)
        search_region = content[vocab_idx:vocab_idx+3000]
        
        # Find the "记忆" (Memory) section, which is the last of the 4 components in current file
        # <span class="font-bold text-amber-500 w-8 shrink-0">记忆</span>
        memory_pattern = '<span class="font-bold text-amber-500 w-8 shrink-0">记忆</span>'
        memory_match = re.search(memory_pattern, search_region)
        
        if memory_match:
            # Find the closing div of the "Memory" row.
            # It starts with <div class="flex items-start gap-2 text-xs">
            # We need to insert AFTER this div closes.
            
            # Locate the start of Memory div
            mem_start_rel = memory_match.start()
            # Find the container div start (scanning backwards from 'Memory' span)
            container_start_rel = search_region.rfind('<div class="flex items-start gap-2 text-xs">', 0, mem_start_rel)
            
            if container_start_rel != -1:
                # Find the closing </div> for this memory container
                # It should be the text-slate-600 span close + div close
                # Simple heuristic: find "</div>" after the memory span text.
                
                # Check if "用法" (Usage) already exists to avoid double injection
                if 'class="font-bold text-emerald-500 w-8 shrink-0">用法</span>' in search_region:
                    print(f"Usage already exists for {vocab}. Skipping injection.")
                    
                    # But we might still need to generate audio if missing...
                    # Let's assume if it exists, we skip for now or we'd parse it like Lesson 3.
                    # For Upgrade, we assume it's missing.
                    continue
                
                # Find where the Memory row ends. 
                # It contains <span class="text-slate-600">...</span> </div>
                
                # Let's find the first </div> AFTER the memory match
                div_close_match = re.search(r'</div>', search_region[mem_start_rel:])
                if div_close_match:
                    insert_point_rel = mem_start_rel + div_close_match.end()
                    
                    # Define Usage HTML
                    audio_filename = f"vocab_usage_{vocab}.mp3"
                    
                    usage_html = f"""
                            <div class="flex items-start gap-2 text-xs">
                                <span class="font-bold text-emerald-500 w-8 shrink-0">用法</span>
                                <span class="text-slate-600 flex items-center gap-2 flex-1">
                                    <span class="flex-1">{sentence}</span>
                                    <button onclick="event.stopPropagation(); playAudio('vocab_usage_{vocab}')"
                                        class="w-6 h-6 rounded-full bg-emerald-50 text-emerald-500 flex items-center justify-center hover:bg-emerald-100 hover:scale-110 transition shadow-sm ml-2 shrink-0">
                                        🔊
                                    </button>
                                </span>
                            </div>"""
                    
                    # Generate Audio
                    clean_text = extract_japanese(sentence)
                    tasks.append(generate_audio(clean_text, audio_filename))
                    
                    # Perform Injection in global content
                    # Calculate absolute insertion point
                    abs_insert_point = vocab_idx + insert_point_rel
                    
                    # We need to be careful about offsets shifting if we modify content in a loop.
                    # Strategy: Store replacements and apply them reverse order or re-read?
                    # Better: Read, Modify Memory, Write Memory.
                    # Since we are iterating, let's just use string replacement on UNIQUE strings if possible.
                    # Or rebuild the file content.
                    # Given the complexity, let's use a "patches" list: (index, string_to_insert)
                    # But index shift is a pain.
                    # Alternative: replace the Memory DIV closing tag `</div>` with `</div>\n{usage_html}`
                    # But `</div>` is not unique. 
                    # The `search_region` is unique enough if we include the vocab title? No.
                    
                    # Re-implementation: Split content? 
                    # Let's try to match the EXACT context for replacement.
                    
                    # Construct valid regex for: Memory Span ... closing </div>
                    # <div class="flex ..."> ... 记忆 ... </div>
                    
                    # We can use `content.replace(original_block, original_block + usage_html)`
                    # We need to capture the `original_block` precisely.
                    
                    # Let's extract the exact string of the Memory block
                    mem_div_start = vocab_idx + container_start_rel
                    mem_div_end = vocab_idx + insert_point_rel
                    
                    original_memory_block = content[mem_div_start:mem_div_end]
                    
                    # Replacement
                    new_memory_block = original_memory_block + "\n" + usage_html
                    
                    # Execute replacement using 'replace' with count=1 to ensure we only target THIS instance?
                    # content.replace(original_memory_block, ...) is risky if identical blocks exist for other words.
                    # But "Memory" content usually differs per word.
                    # Let's verify: "记忆" ... "本" -> "这本书是红色的"
                    # Yes, memory content is unique per word usually.
                    
                    content = content[:mem_div_start] + new_memory_block + content[mem_div_end:]
                    
                    # Note: indices for subsequent words (which are further down) will shift by len(usage_html).
                    # This implies valid loop order or tracking offset.
                    # Since we iterate generic dictionary, order isn't guaranteed match file order.
                    # Safer approach: Split file, append, join? 
                    # Or simpler: Just Run the script multiple times? No.
                    
                    # Best Approach: Use a `offset` variable.
                    # We need to process words IN ORDER of appearance in file.
                    # So, let's find all vocab locations first, sort them, then process.
    
    # Pre-scan for all vocab locations
    vocab_locations = []
    for vocab, sentence in USAGE_DATA.items():
        vocab_pattern = f'<span class="text-[1-4]?xl font-bold text-slate-800">{vocab}</span>'
        vocab_match = re.search(vocab_pattern, content)
        if vocab_match:
            vocab_locations.append({
                "vocab": vocab,
                "sentence": sentence,
                "index": vocab_match.start()
            })
    
    # Sort by index descending (bottom up) to avoid index shift issues
    vocab_locations.sort(key=lambda x: x['index'], reverse=True)
    
    for item in vocab_locations:
        vocab = item['vocab']
        sentence = item['sentence']
        idx = item['index']
        
        # Local search region (scanning forward from idx)
        # We need to be careful not to rely on `content` slices if we are modifying it?
        # Since we modify from Bottom-Up, existing `idx` for lower items are valid.
        
        search_region = content[idx:idx+3000]
        
        memory_pattern = '<span class="font-bold text-amber-500 w-8 shrink-0">记忆</span>'
        memory_match = re.search(memory_pattern, search_region)
        
        if memory_match:
             mem_start_rel = memory_match.start()
             # Find container start. Supports text-xs or text-[10px]
             # Hard to use rfind with regex. Scan backwards manual or strict match?
             # Let's try finding the class string.
             
             # Search backwards for <div class="flex 
             container_start_rel = search_region.rfind('<div class="flex items-start gap-2 text-', 0, mem_start_rel)
             
             if container_start_rel != -1:
                 # It matched the prefix.
                 # Check if it continues with xs"> OR [10px]">
                 # Actually we just need the start index of the DIV tag.
                 pass

                 # Find closing div
                 div_close_match = re.search(r'</div>', search_region[mem_start_rel:])
                 if div_close_match:
                     block_end_rel = mem_start_rel + div_close_match.end()
                     
                     # Check existence
                     if 'class="font-bold text-emerald-500 w-8 shrink-0">用法</span>' in search_region[:block_end_rel+200]:
                         print(f"Skipping HTML for {vocab}, Usage exists.")
                         # Check Audio
                         audio_filename = f"vocab_usage_{vocab}.mp3"
                         output_path = os.path.join(os.path.dirname(__file__), AUDIO_OUTPUT_DIR, audio_filename)
                         if not os.path.exists(output_path):
                             print(f"Audio missing for {vocab}, adding task.")
                             clean_text = extract_japanese(sentence)
                             tasks.append(generate_audio(clean_text, audio_filename))
                         continue
                         
                     # Generate Audio
                     audio_filename = f"vocab_usage_{vocab}.mp3"
                     clean_text = extract_japanese(sentence)
                     tasks.append(generate_audio(clean_text, audio_filename))
                     
                     # HTML Payload
                     usage_html = f"""
                            <div class="flex items-start gap-2 text-xs">
                                <span class="font-bold text-emerald-500 w-8 shrink-0">用法</span>
                                <span class="text-slate-600 flex items-center gap-2 flex-1">
                                    <span class="flex-1">{sentence}</span>
                                    <button onclick="event.stopPropagation(); playAudio('vocab_usage_{vocab}')"
                                        class="w-6 h-6 rounded-full bg-emerald-50 text-emerald-500 flex items-center justify-center hover:bg-emerald-100 hover:scale-110 transition shadow-sm ml-2 shrink-0">
                                        🔊
                                    </button>
                                </span>
                            </div>"""
                     
                     # Splice content
                     # absolute end index
                     abs_block_end = idx + block_end_rel
                     
                     content = content[:abs_block_end] + usage_html + content[abs_block_end:]
                     print(f"Injected Usage for {vocab}")

    # Write updated HTML
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # Run Audio Tasks
    if tasks:
        print("Generating audio files...")
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
