
import os

TARGET_FILE = "chapter2_lesson2.html"

# Missing Cards Data
# Template: {KANJI}, {KANA}, {MEANING_CN}, {MEANING_EN}, {TONE}, {COMPONENT}, {MEMORY}, {ROMAJI}
NEW_CARDS = [
    {
        "kanji": "辞書",
        "kana": "じしょ",
        "meaning_cn": "词典",
        "meaning_en": "Dictionary",
        "tone": "①",
        "component": "辞 (Words) + 書 (Book)",
        "memory": "辞書で言葉を調べます。",
        "romaji": "jisho"
    },
    {
        "kanji": "雑誌",
        "kana": "ざっし",
        "meaning_cn": "杂志",
        "meaning_en": "Magazine",
        "tone": "⓪",
        "component": "雑 (Misc) + 誌 (Record)",
        "memory": "雑誌は面白いです。",
        "romaji": "zasshi"
    },
    {
        "kanji": "電話",
        "kana": "でんわ",
        "meaning_cn": "电话",
        "meaning_en": "Telephone",
        "tone": "⓪",
        "component": "電 (Electricity) + 話 (Talk)",
        "memory": "電話で話します。",
        "romaji": "denwa"
    }
]

def generate_card_html(card):
    return f"""
                    <!-- {card['meaning_en']} -->
                    <div class="glass-panel p-6 group cursor-pointer hover:bg-white/80 transition">
                        <div class="flex justify-between items-start mb-2">
                            <span class="text-2xl font-bold text-slate-800">{card['kanji']}</span>
                            <div class="flex items-center gap-2">
                                <span class="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded-lg">{card['tone']}</span>
                                <button onclick="playAudio('{card['romaji']}')"
                                    class="text-slate-400 hover:text-indigo-500 transition">🔊</button>
                            </div>
                        </div>
                        <div class="flex justify-between items-end">
                            <div>
                                <p class="text-sm text-slate-500 font-mono">{card['kana']}</p>
                                <p class="text-lg font-medium text-slate-600">{card['meaning_cn']} ({card['meaning_en']})</p>
                            </div>
                        </div>
                        <div class="mt-4 pt-3 border-t border-slate-200/50 space-y-2">
                            <div class="flex items-start gap-2 text-xs">
                                <span class="font-bold text-slate-400 w-8 shrink-0">构词</span>
                                <span class="text-slate-600">{card['component']}</span>
                            </div>
                            <div class="flex items-start gap-2 text-xs">
                                <span class="font-bold text-amber-500 w-8 shrink-0">记忆</span>
                                <span class="text-slate-600">{card['memory']}</span>
                            </div>
                        </div>
                    </div>"""

def main():
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Vocabulary Grid text-slate-500">(Core Vocabulary)</span>
    # Then find the grid div after that.
    
    start_marker = "(Items & Objects)</span>"
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print("Error: Vocabulary section not found.")
        return

    # Find the grid start
    grid_start_idx = content.find('<div class="grid', start_idx)
    
    # We need to find the CLOSING div of this grid.
    # This is tricky without parsing.
    # But usually the grid is indented.
    # Let's assume the grid ends before the NEXT section header?
    # Or count divs?
    
    # Let's insert them at the BEGINNING of the grid for visibility, or after the first item?
    # Or just Append.
    
    # Simpler strategy:
    # Just insert them after the opening tag of the grid.
    # <div class="grid ... gap-6">
    # {INSERT HERE}
    
    insertion_point = content.find('>', grid_start_idx) + 1
    
    vocab_html = ""
    for card in NEW_CARDS:
        # Check if already exists to avoid dupes
        if f'>{card["kanji"]}<' in content:
            print(f"Skipping {card['kanji']}, already exists.")
            continue
            
        vocab_html += generate_card_html(card)
        print(f"Added {card['kanji']}")
        
    if vocab_html:
        new_content = content[:insertion_point] + vocab_html + content[insertion_point:]
        
        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Injection complete.")
    else:
        print("No new cards added.")

if __name__ == "__main__":
    main()
