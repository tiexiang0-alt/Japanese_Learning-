
import os
import asyncio
import edge_tts

# Define the Master Scene Dialogue
dialogue_part1 = [
    {
        "id": "master_1_1",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "すみません、ネクタイ売り場はどこですか。",
        "en": "Excuse me, where is the necktie section?"
    },
    {
        "id": "master_1_2",
        "speaker": "店員",
        "speaker_full": "店員 (Staff)",
        "snippet": "S",
        "bg_color": "bg-slate-200",
        "text_color": "text-slate-500",
        "side": "right",
        "jp": "三階です。エスカレーターはあちらです。",
        "en": "It is on the 3rd floor. The escalator is over there."
    },
    {
        "id": "master_1_3",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "どうもありがとうございます。",
        "en": "Thank you very much."
    },
    {
        "id": "master_1_4",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "すみません、これはどこのネクタイですか。",
        "en": "Excuse me, where is this necktie from?"
    },
    {
        "id": "master_1_5",
        "speaker": "店員",
        "speaker_full": "店員 (Staff)",
        "snippet": "S",
        "bg_color": "bg-slate-200",
        "text_color": "text-slate-500",
        "side": "right",
        "jp": "それはイタリアのネクタイです。",
        "en": "That is an Italian necktie."
    },
    {
        "id": "master_1_6",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "いくらですか。",
        "en": "How much is it?"
    },
    {
        "id": "master_1_7",
        "speaker": "店員",
        "speaker_full": "店員 (Staff)",
        "snippet": "S",
        "bg_color": "bg-slate-200",
        "text_color": "text-slate-500",
        "side": "right",
        "jp": "一万五千円です。",
        "en": "It is 15,000 yen."
    },
    {
        "id": "master_1_8",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "ちょっと高いですね。じゃ、あれは？",
        "en": "It is a bit expensive. Then, how about that one?"
    },
    {
        "id": "master_1_9",
        "speaker": "店員",
        "speaker_full": "店員 (Staff)",
        "snippet": "S",
        "bg_color": "bg-slate-200",
        "text_color": "text-slate-500",
        "side": "right",
        "jp": "あれは日本のネクタイです。五千八百円です。",
        "en": "That is a Japanese necktie. It is 5,800 yen."
    },
    {
        "id": "master_1_10",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "そうですか。じゃ、あれをください。",
        "en": "I see. Then, I will take that one."
    },
    {
        "id": "master_1_11",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "このハンカチもください。",
        "en": "Please give me this handkerchief too."
    },
    {
        "id": "master_1_12",
        "speaker": "店員",
        "speaker_full": "店員 (Staff)",
        "snippet": "S",
        "bg_color": "bg-slate-200",
        "text_color": "text-slate-500",
        "side": "right",
        "jp": "はい。全部で七千円です。",
        "en": "Yes. That will be 7,000 yen in total."
    }
]

dialogue_part2 = [
    {
        "id": "master_2_1",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "ここは静かですね。",
        "en": "It is quiet here, isn't it?"
    },
    {
        "id": "master_2_2",
        "speaker": "佐藤",
        "speaker_full": "佐藤 (Sato)",
        "snippet": "Sa",
        "bg_color": "bg-emerald-100",
        "text_color": "text-emerald-500",
        "side": "right",
        "jp": "ええ。この周辺はとても便利です。",
        "en": "Yes. This area (surroundings) is very convenient."
    },
    {
        "id": "master_2_3",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "あの建物はホテルですか。",
        "en": "Is that building a hotel?"
    },
    {
        "id": "master_2_4",
        "speaker": "佐藤",
        "speaker_full": "佐藤 (Sato)",
        "snippet": "Sa",
        "bg_color": "bg-emerald-100",
        "text_color": "text-emerald-500",
        "side": "right",
        "jp": "いいえ、あれはマンションです。ホテルは隣です。",
        "en": "No, that is a high-rise apartment. The hotel is next to it."
    },
    {
        "id": "master_2_5",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "郵便局はどこですか。",
        "en": "Where is the post office?"
    },
    {
        "id": "master_2_6",
        "speaker": "佐藤",
        "speaker_full": "佐藤 (Sato)",
        "snippet": "Sa",
        "bg_color": "bg-emerald-100",
        "text_color": "text-emerald-500",
        "side": "right",
        "jp": "郵便局はあそこです。銀行の隣です。",
        "en": "The post office is over there. Next to the bank."
    },
    {
        "id": "master_2_7",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "図書館もありますか。",
        "en": "Is there also a library?"
    },
    {
        "id": "master_2_8",
        "speaker": "佐藤",
        "speaker_full": "佐藤 (Sato)",
        "snippet": "Sa",
        "bg_color": "bg-emerald-100",
        "text_color": "text-emerald-500",
        "side": "right",
        "jp": "ええ。でも、今日は水曜日ですね。休みです。",
        "en": "Yes. But today is Wednesday, right? It is closed."
    },
    {
        "id": "master_2_9",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "そうですか。事務所は何階ですか。",
        "en": "I see. What floor is the office on?"
    },
    {
        "id": "master_2_10",
        "speaker": "佐藤",
        "speaker_full": "佐藤 (Sato)",
        "snippet": "Sa",
        "bg_color": "bg-emerald-100",
        "text_color": "text-emerald-500",
        "side": "right",
        "jp": "事務所は二階です。受付はこちらです。",
        "en": "The office is on the 2nd floor. Reception is this way."
    },
    {
        "id": "master_2_11",
        "speaker": "王",
        "speaker_full": "王 (Wang)",
        "snippet": "W",
        "bg_color": "bg-indigo-100",
        "text_color": "text-indigo-500",
        "side": "left",
        "jp": "食堂はどこですか。",
        "en": "Where is the canteen?"
    },
    {
        "id": "master_2_12",
        "speaker": "佐藤",
        "speaker_full": "佐藤 (Sato)",
        "snippet": "Sa",
        "bg_color": "bg-emerald-100",
        "text_color": "text-emerald-500",
        "side": "right",
        "jp": "食堂は地下です。安いです。",
        "en": "The canteen is in the basement. It is cheap."
    }
]

full_dialogue = dialogue_part1 + dialogue_part2

def render_scene_block(dialogue_list, title, subtitle):
    blocks = []
    header = f"""
        <div class="mb-8">
            <h3 class="text-xl font-bold text-slate-700 mb-4 pl-4 border-l-4 border-indigo-400">{title}</h3>
            <p class="text-sm text-slate-500 mb-6">{subtitle}</p>
            <div class="space-y-6">
    """
    blocks.append(header)
    
    for line in dialogue_list:
        if line["side"] == "left":
            flex_class = ""
            bubble_class = "chat-bubble chat-left"
        else:
            flex_class = "flex-row-reverse"
            bubble_class = "chat-bubble chat-right"
            
        block = f"""
                <div class="flex gap-4 items-end group cursor-pointer {flex_class}" onclick="playAudio('{line['id']}')">
                    <div class="w-16 h-16 rounded-2xl {line['bg_color']} flex items-center justify-center font-bold {line['text_color']} text-2xl shadow-sm">
                        {line['snippet']}
                    </div>
                    <div class="{bubble_class} group-hover:scale-[1.02] transition-transform shadow-md">
                        <p class="text-lg font-bold">{line['jp']} 🔊</p>
                        <p class="text-sm mt-2 opacity-80">{line['en']}</p>
                    </div>
                </div>
        """
        blocks.append(block)
        
    blocks.append("</div></div>")
    return "\n".join(blocks)

def generate_html():
    html_parts = []
    
    header = """
            <!-- Master Scene -->
            <div class="glass-panel p-10 relative overflow-hidden mb-12 border-4 border-indigo-100" id="master-dialogue-container">
                <div class="absolute top-0 right-0 p-4 opacity-10">
                    <span class="text-9xl font-black text-indigo-900">総</span>
                </div>
                <h2 class="text-3xl font-black text-slate-800 mb-4 flex items-center gap-4 relative z-10">
                    <span class="bg-gradient-to-r from-indigo-500 to-purple-600 px-4 py-1 rounded-xl text-sm text-white shadow-lg">FINAL MIX</span>
                    综合演练 (Master Dialogue)
                </h2>
                <p class="mb-10 text-slate-600 relative z-10">
                    A comprehensive dialogue covering 100% of the lesson vocabulary and grammar.
                </p>

                <div class="relative z-10">
    """
    html_parts.append(header)
    
    html_parts.append(render_scene_block(dialogue_part1, "Part 1: Shopping (お買い物)", "Target: Shopping vocab, Prices, Origin, Choice."))
    html_parts.append("<div class='h-px bg-slate-200 my-8'></div>")
    html_parts.append(render_scene_block(dialogue_part2, "Part 2: Facility Tour (施設案内)", "Target: Facilities, Locations, Days of Week."))
    
    footer = """
                </div>
            </div>
    """
    html_parts.append(footer)
    
    return "\n".join(html_parts)

async def generate_audio_files():
    base_dir = "/Users/hardentie/Downloads/vscode/learning/japanese/assets/audio/lesson3"
    os.makedirs(base_dir, exist_ok=True)
    
    tasks = []
    for line in full_dialogue:
        filename = f"{line['id']}.mp3"
        filepath = os.path.join(base_dir, filename)
        
        # Optimization: Check if file exists? No, regenerate to be safe.
        
        # Choose voice
        if line["speaker"] == "店員" or line["speaker"] == "佐藤":
            voice = "ja-JP-NanamiNeural" # Female
        else:
            voice = "ja-JP-KeitaNeural" # Male
            
        print(f"Generating {filename} with voice {voice}...")
        communicate = edge_tts.Communicate(line["jp"], voice)
        tasks.append(communicate.save(filepath))
        
    await asyncio.gather(*tasks)

def main():
    # 1. Generate HTML
    html_content = generate_html()
    with open("lesson3_master_scene.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated lesson3_master_scene.html")
    
    # 2. Generate Audio
    asyncio.run(generate_audio_files())
    print("Generated Audio Files")

if __name__ == "__main__":
    main()
