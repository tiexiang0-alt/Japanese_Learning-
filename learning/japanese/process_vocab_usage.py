
import os
import re
import asyncio
import edge_tts

# Audio settings
VOICE = "ja-JP-NanamiNeural"
AUDIO_DIR = "assets/audio/lesson3"

def extract_japanese(text):
    # First: Remove <rt>...</rt> tags AND their content (the reading)
    # Use re.DOTALL if multiline, but here single line is expected mostly.
    clean_text = re.sub(r'<rt>.*?</rt>', '', text)
    # Second: Remove remaining HTML tags (e.g. <ruby>, <span>)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    # Extract text before the first opening parenthesis '(', or return full text
    match = re.match(r'^(.*?)(?:\(|（)', clean_text)
    if match:
        return match.group(1).strip()
    return clean_text.strip()

async def generate_audio(text, filename):
    output_path = os.path.join("/Users/hardentie/Downloads/vscode/learning/japanese", AUDIO_DIR, filename)
    # Check if exists? Overwrite for safety.
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)
    print(f"Generated: {filename}")

async def process_vocab_usage():
    base_dir = '/Users/hardentie/Downloads/vscode/learning/japanese'
    html_path = os.path.join(base_dir, 'chapter2_lesson3.html')
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Pattern to find Vocabulary Cards
    # We look for onclick="playAudio('vocab_NAME')"
    # Then inside that block we look for "用法" (Usage)
    # The structure allows us to regex match the whole card or iterate.
    
    # Let's split by "playAudio('vocab_" to iterate through potential cards?
    # Or use a robust regex.
    
    # Regex to capture:
    # 1. Vocab Term (from onclick)
    # 2. Everything until the Usage section
    # 3. The Usage text content
    
    # Since HTML is large, we should be careful.
    # Let's iterate over `onclick="playAudio('vocab_(.*?)')"`
    
    # We will build a list of replacements to make.
    # (Start Index, End Index, New Content) -> But string indices change.
    # Better: use string replace if content is unique. "用法" content is usually unique sentences.
    
    # Let's verify if we can find the usage span AFTER the vocab click.
    # We can perform a split-based parsing.
    
    cards = html.split('onclick="playAudio(\'vocab_')
    
    new_html_parts = [cards[0]]
    tasks = []
    
    # Iterate from 1 onwards
    for i in range(1, len(cards)):
        part = cards[i]
        # part starts with "TERM')"> ... content ...
        
        # 1. Extract Term
        term_end = part.find("')")
        term = part[:term_end]
        
        # 2. Look for Usage Section inside this part (before the next card starts)
        # Usage marker: <span class="font-bold text-emerald-500 w-8 shrink-0">用法</span>
        usage_marker = '用法</span>'
        usage_idx = part.find(usage_marker)
        
        if usage_idx != -1:
            # Substring from usage_idx
            usage_context = part[usage_idx:]
            
            # Check for modified structure first
            # New structure: <span class="flex-1">TEXT</span> inside the block
            # Original: <span class="text-slate-600">TEXT</span>
            
            content_match = re.search(r'<span class="flex-1">(.*?)</span>', usage_context)
            if not content_match:
                 # Fallback to original
                 content_match = re.search(r'<span class="text-slate-600">(.*?)</span>', usage_context)
            
            if content_match:
                # original_span reference is tricky if we switched regex, but we only used it for replacement
                # If we are in modified structure, we don't need to replace HTML, just generate Audio.
                
                usage_text_full = content_match.group(1)
                
                # Extract Japanese for TTS
                jp_text = extract_japanese(usage_text_full)
                
                # Generate Audio Filename
                audio_filename = f"vocab_usage_{term}.mp3"
                
                # Queue Audio Generation ALWAYS (since we want to overwrite bad audio)
                if jp_text:
                    print(f"Generating audio for '{term}': '{jp_text}'")
                    tasks.append(generate_audio(jp_text, audio_filename))
                
                # Only inject HTML if not present
                if "playAudio('vocab_usage_" not in usage_context:
                    # We need the ORIGINAL span to replace it.
                    # Rerun regex for original span to get start/end indices relative to usage_context
                    fallback_match = re.search(r'<span class="text-slate-600">(.*?)</span>', usage_context)
                    if fallback_match:
                         # ... (Perform replacement logic)
                         pass # The logic below needs to be inside this block or adjusted.
                         
                         # Let's adjust the flow:
                         original_span_text = fallback_match.group(0)
                         new_inner_html = f"""
                            <span class="flex-1">{usage_text_full}</span>
                            <button onclick="event.stopPropagation(); playAudio('{audio_filename}')" 
                                    class="w-6 h-6 rounded-full bg-emerald-50 text-emerald-500 flex items-center justify-center hover:bg-emerald-100 hover:scale-110 transition shadow-sm ml-2 shrink-0">
                                🔊
                            </button>
                        """
                         new_span = f'<span class="text-slate-600 flex items-center gap-2 flex-1">{new_inner_html}</span>'
                         
                         span_start = usage_idx + fallback_match.start()
                         span_end = usage_idx + fallback_match.end()
                         part = part[:span_start] + new_span + part[span_end:]
        
        new_html_parts.append(part)
        
    # Reassemble HTML
    final_html = 'onclick="playAudio(\'vocab_'.join(new_html_parts)
    
    # Save HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    # Generate Audio
    if tasks:
        print(f"Generating {len(tasks)} usage audio files...")
        await asyncio.gather(*tasks)
    else:
        print("No new usage audio to generate.")

if __name__ == "__main__":
    if not os.path.exists("/Users/hardentie/Downloads/vscode/learning/japanese/" + AUDIO_DIR):
        os.makedirs("/Users/hardentie/Downloads/vscode/learning/japanese/" + AUDIO_DIR)
    asyncio.run(process_vocab_usage())
