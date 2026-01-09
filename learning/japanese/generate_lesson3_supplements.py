import os

def generate_vocab_html(vocab_list):
    html = []
    for vocab in vocab_list:
        card = f"""
                <!-- {vocab['word']} -->
                <div class="glass-panel p-6 group cursor-pointer hover:shadow-xl transition-all duration-300" onclick="playAudio('vocab_{vocab['word']}')">
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <span class="text-3xl font-bold text-slate-800">{vocab['word']} 
                                <span class="text-lg text-indigo-500">🔊</span>
                            </span>
                            <div class="text-indigo-600 font-bold mt-2 text-xl tracking-widest">
                                {vocab['kana']}
                            </div>
                        </div>
                        <span class="px-3 py-1 bg-white/80 text-slate-800 border border-slate-300 text-xs rounded-full font-bold">TYPE {vocab['type']}</span>
                    </div>
                    
                    <!-- English Meaning -->
                    <div class="p-3 bg-blue-50 rounded-xl border border-blue-100 mb-3">
                        <p class="text-sm font-bold text-blue-700">{vocab['meaning']}</p>
                        <p class="text-xs text-blue-500 mt-1">{vocab['category']}</p>
                    </div>
                    
                    <!-- 5 Components -->
                    <div class="mt-4 pt-3 border-t border-slate-200/50 space-y-2">
                        <div class="flex items-start gap-2 text-xs">
                            <span class="font-bold text-slate-400 w-8 shrink-0">构词</span>
                            <span class="text-slate-600">{vocab['structure']}</span>
                        </div>
                        <div class="flex items-start gap-2 text-xs">
                            <span class="font-bold text-slate-400 w-8 shrink-0">词源</span>
                            <span class="text-slate-600">{vocab['etymology']}</span>
                        </div>
                        <div class="flex items-start gap-2 text-xs">
                            <span class="font-bold text-amber-500 w-8 shrink-0">记忆</span>
                            <span class="text-slate-600">{vocab['mnemonic']}</span>
                        </div>
                        <div class="flex items-start gap-2 text-xs">
                            <span class="font-bold text-emerald-500 w-8 shrink-0">用法</span>
                            <span class="text-slate-600">{vocab['usage']}</span>
                        </div>
                    </div>
                </div>"""
        html.append(card)
    return "\n".join(html)

def generate_grammar_html():
    grammar_html = """
            <!-- Grammar Point: Polite Place Pronouns -->
            <div class="glass-panel p-8 mb-8 relative overflow-hidden">
                <div class="absolute top-0 right-0 p-8 opacity-5">
                    <span class="text-9xl font-black text-indigo-900">禮</span>
                </div>
                <h3 class="text-2xl font-black text-indigo-800 mb-6 flex items-center gap-3 relative z-10">
                    <span class="flex items-center justify-center w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 text-lg">6</span>
                    礼貌方位词 (Polite Direction/Place Words)
                </h3>
                
                <div class="space-y-6 relative z-10">
                    <div class="p-4 bg-indigo-50/50 rounded-2xl border border-indigo-100">
                        <p class="text-slate-700 leading-relaxed mb-4">
                            In formal situations, use <span class="font-bold text-indigo-600">こちら (kochira)</span>, <span class="font-bold text-indigo-600">そちら (sochira)</span>, and <span class="font-bold text-indigo-600">あちら (achira)</span> instead of koko/soko/asoko. They literally mean "this direction" but are used to refer to places or people politely.
                        </p>
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                            <div class="bg-white p-3 rounded-xl border border-indigo-100 text-center">
                                <span class="block text-xs text-slate-400 mb-1">Here / This person</span>
                                <span class="text-lg font-bold text-slate-800">こちら</span>
                                <span class="block text-xs text-indigo-500 mt-1">kochira</span>
                            </div>
                            <div class="bg-white p-3 rounded-xl border border-indigo-100 text-center">
                                <span class="block text-xs text-slate-400 mb-1">There / That person</span>
                                <span class="text-lg font-bold text-slate-800">そちら</span>
                                <span class="block text-xs text-indigo-500 mt-1">sochira</span>
                            </div>
                            <div class="bg-white p-3 rounded-xl border border-indigo-100 text-center">
                                <span class="block text-xs text-slate-400 mb-1">Over there / That person</span>
                                <span class="text-lg font-bold text-slate-800">あちら</span>
                                <span class="block text-xs text-indigo-500 mt-1">achira</span>
                            </div>
                        </div>

                        <ul class="space-y-3">
                            <li class="flex items-start gap-3 bg-white p-3 rounded-xl shadow-sm cursor-pointer hover:shadow-md transition" onclick="playAudio('grammar_6_1')">
                                <span class="text-xl">👩‍💼</span>
                                <div>
                                    <p class="font-bold text-slate-800 text-lg">こちらは田中さんです。</p>
                                    <p class="text-slate-500 text-sm">This is Mr./Ms. Tanaka. (Polite introduction)</p>
                                </div>
                            </li>
                            <li class="flex items-start gap-3 bg-white p-3 rounded-xl shadow-sm cursor-pointer hover:shadow-md transition" onclick="playAudio('grammar_6_2')">
                                <span class="text-xl">🏢</span>
                                <div>
                                    <p class="font-bold text-slate-800 text-lg">お手洗いはあちらです。</p>
                                    <p class="text-slate-500 text-sm">The restroom is over there. (Polite direction)</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Grammar Point: Particle Mo -->
            <div class="glass-panel p-8 mb-8 relative overflow-hidden">
                <div class="absolute top-0 right-0 p-8 opacity-5">
                    <span class="text-9xl font-black text-rose-900">も</span>
                </div>
                <h3 class="text-2xl font-black text-rose-800 mb-6 flex items-center gap-3 relative z-10">
                    <span class="flex items-center justify-center w-10 h-10 rounded-full bg-rose-100 text-rose-600 text-lg">7</span>
                    助词 "も" (Particle Mo - Also/Too)
                </h3>
                
                <div class="space-y-6 relative z-10">
                    <div class="p-4 bg-rose-50/50 rounded-2xl border border-rose-100">
                        <p class="text-slate-700 leading-relaxed mb-4">
                            Use <span class="font-bold text-rose-600">も (mo)</span> instead of <span class="font-bold text-slate-400">は (wa)</span> when the topic applies to the same predicate as the previous statement. It corresponds to "also" or "too" in English.
                        </p>
                        
                        <div class="p-4 bg-white/80 rounded-xl border border-rose-100 mb-4 text-center">
                            <span class="text-xl font-bold text-slate-600">Topic A <span class="text-rose-400">は</span> ...。 Topic B <span class="text-rose-600 font-black text-2xl">も</span> ...。</span>
                        </div>

                        <ul class="space-y-3">
                            <li class="flex items-start gap-3 bg-white p-3 rounded-xl shadow-sm cursor-pointer hover:shadow-md transition" onclick="playAudio('grammar_7_1')">
                                <span class="text-xl">🇨🇳</span>
                                <div>
                                    <p class="font-bold text-slate-800 text-lg">私は中国人です。周さんも中国人です。</p>
                                    <p class="text-slate-500 text-sm">I am Chinese. Mr. Zhou is <span class="font-bold text-rose-600">also</span> Chinese.</p>
                                </div>
                            </li>
                            <li class="flex items-start gap-3 bg-white p-3 rounded-xl shadow-sm cursor-pointer hover:shadow-md transition" onclick="playAudio('grammar_7_2')">
                                <span class="text-xl">🖊️</span>
                                <div>
                                    <p class="font-bold text-slate-800 text-lg">これも日本のペンですね。</p>
                                    <p class="text-slate-500 text-sm">This is <span class="font-bold text-rose-600">also</span> a Japanese pen, isn't it?</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Grammar Point: Choice Questions -->
            <div class="glass-panel p-8 mb-8 relative overflow-hidden">
                <div class="absolute top-0 right-0 p-8 opacity-5">
                    <span class="text-9xl font-black text-emerald-900">選</span>
                </div>
                <h3 class="text-2xl font-black text-emerald-800 mb-6 flex items-center gap-3 relative z-10">
                    <span class="flex items-center justify-center w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 text-lg">8</span>
                    选择疑问句 (Choice Questions)
                </h3>
                
                <div class="space-y-6 relative z-10">
                    <div class="p-4 bg-emerald-50/50 rounded-2xl border border-emerald-100">
                        <p class="text-slate-700 leading-relaxed mb-4">
                            To ask "Is it A or B?", simply list two questions connected by distinct pauses (commas). <br>
                            <span class="font-bold text-red-500">Crucial Rule:</span> Do NOT answer with "Hai" or "Iie". State the correct option directly.
                        </p>
                        
                        <div class="p-4 bg-white/80 rounded-xl border border-emerald-100 mb-4 text-center">
                            <span class="text-lg font-bold text-slate-600">S1 <span class="text-emerald-500">ですか</span>、 S2 <span class="text-emerald-500">ですか</span>。</span>
                        </div>

                        <ul class="space-y-3">
                            <li class="flex items-start gap-3 bg-white p-3 rounded-xl shadow-sm cursor-pointer hover:shadow-md transition" onclick="playAudio('grammar_8_1')">
                                <span class="text-xl">📅</span>
                                <div>
                                    <p class="font-bold text-slate-800 text-lg">今日は水曜日ですか、木曜日ですか。</p>
                                    <p class="text-slate-500 text-sm">Is today Wednesday or Thursday?</p>
                                    <p class="text-emerald-600 font-bold mt-1 text-sm">→ 水曜日です。(It's Wednesday.)</p>
                                </div>
                            </li>
                            <li class="flex items-start gap-3 bg-white p-3 rounded-xl shadow-sm cursor-pointer hover:shadow-md transition" onclick="playAudio('grammar_8_2')">
                                <span class="text-xl">🏬</span>
                                <div>
                                    <p class="font-bold text-slate-800 text-lg">ここは一階ですか、二階ですか。</p>
                                    <p class="text-slate-500 text-sm">Is this the 1st floor or the 2nd floor?</p>
                                    <p class="text-emerald-600 font-bold mt-1 text-sm">→ 二階です。(It's the 2nd floor.)</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Grammar Point: Asking Price -->
            <div class="glass-panel p-8 mb-8 relative overflow-hidden">
                <div class="absolute top-0 right-0 p-8 opacity-5">
                    <span class="text-9xl font-black text-amber-900">￥</span>
                </div>
                <h3 class="text-2xl font-black text-amber-800 mb-6 flex items-center gap-3 relative z-10">
                    <span class="flex items-center justify-center w-10 h-10 rounded-full bg-amber-100 text-amber-600 text-lg">9</span>
                    询问价格 (Asking Price)
                </h3>
                
                <div class="space-y-6 relative z-10">
                    <div class="p-4 bg-amber-50/50 rounded-2xl border border-amber-100">
                        <p class="text-slate-700 leading-relaxed mb-4">
                            Use the question word <span class="font-bold text-amber-600">いくら (ikura)</span> to ask "How much?".
                        </p>
                        
                        <div class="p-4 bg-white/80 rounded-xl border border-amber-100 mb-4 text-center">
                            <span class="text-xl font-bold text-slate-600"><span class="text-slate-400 font-normal">Noun</span> は いくらですか。</span>
                        </div>

                        <ul class="space-y-3">
                            <li class="flex items-start gap-3 bg-white p-3 rounded-xl shadow-sm cursor-pointer hover:shadow-md transition" onclick="playAudio('grammar_9_1')">
                                <span class="text-xl">👜</span>
                                <div>
                                    <p class="font-bold text-slate-800 text-lg">このかばんはいくらですか。</p>
                                    <p class="text-slate-500 text-sm">How much is this bag?</p>
                                    <p class="text-amber-600 font-bold mt-1 text-sm">→ 5800円です。(It's 5,800 yen.)</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
    """
    return grammar_html

def generate_culture_html():
    culture_html = """
            <!-- Cultural Note: Toilet Etiquette -->
            <section class="space-y-6 mt-12">
                <h3 class="text-2xl font-black text-slate-800 mb-6 pl-4 border-l-8 border-pink-400 flex items-center gap-3">
                    🚽 日本洗手间文化 <span class="text-sm font-normal text-slate-500">(Toilets in Japan)</span>
                </h3>
                <div class="glass-panel p-8">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="p-6 bg-pink-50 rounded-2xl border border-pink-100">
                            <h4 class="font-bold text-pink-600 text-lg mb-2">音姬 (Otohime)</h4>
                            <p class="text-sm text-slate-600 leading-relaxed">
                                Many Japanese toilets have a button or sensor marked <span class="font-bold">「音姫」</span> (Sound Princess). It plays flushing water sounds to mask any embarrassing noises, saving actual water!
                            </p>
                        </div>
                        <div class="p-6 bg-indigo-50 rounded-2xl border border-indigo-100">
                            <h4 class="font-bold text-indigo-600 text-lg mb-2">Toilet Paper Rule</h4>
                            <p class="text-sm text-slate-600 leading-relaxed">
                                Unlike in some countries, Japanese toilet paper is water-soluble. <span class="font-bold text-red-500">Always flush it</span> down the toilet. Do NOT put used paper in the small trash bin (that's for hygiene products only).
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Cultural Note: Shopping -->
            <section class="space-y-6 mt-12">
                <h3 class="text-2xl font-black text-slate-800 mb-6 pl-4 border-l-8 border-yellow-400 flex items-center gap-3">
                    🛍️ 购物小贴士 <span class="text-sm font-normal text-slate-500">(Shopping Tips)</span>
                </h3>
                <div class="glass-panel p-8">
                    <div class="flex flex-col gap-4">
                        <div class="p-4 bg-yellow-50 rounded-xl border border-yellow-100">
                            <h4 class="font-bold text-yellow-700 mb-1">Tax-Free Shopping (免税)</h4>
                            <p class="text-sm text-slate-600">
                                Look for "Tax-Free" signs. Consumption tax is 10%, but tourists can get it refunded on purchases over 5,000-5,500 JPY. Always bring your passport!
                            </p>
                        </div>
                        <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
                            <h4 class="font-bold text-slate-700 mb-1">Electronics Giants</h4>
                            <p class="text-sm text-slate-600">
                                For electronics, visit <span class="font-bold text-blue-600">Bic Camera</span> (ビックカメラ) or <span class="font-bold text-slate-800">Yodobashi Camera</span> (ヨドバシカメラ). They often offer additional discounts for certain credit cards alongside tax-free benefits.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Cultural Note: Days of Week -->
            <section class="space-y-6 mt-12">
                <h3 class="text-2xl font-black text-slate-800 mb-6 pl-4 border-l-8 border-cyan-400 flex items-center gap-3">
                    🗓️ 星期记忆法 <span class="text-sm font-normal text-slate-500">(Days Mnemonics)</span>
                </h3>
                <div class="glass-panel p-8">
                    <p class="mb-4 text-slate-600">Simple ways to remember Wednesday and Thursday based on Kanji characters:</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="p-6 bg-cyan-50 rounded-2xl border border-cyan-100">
                            <h4 class="font-bold text-cyan-700 text-3xl mb-2">水曜日 <span class="text-sm text-cyan-500 block mt-1">Wednesday</span></h4>
                            <p class="text-sm text-slate-600">
                                <span class="font-bold">水 (Water)</span>. Imagine the middle of the week is wet like water.
                                <br>Mnemonic: "Water Wednesday". Also, the kanji for water (水) looks a bit like 3 lines -> 3rd day.
                            </p>
                        </div>
                        <div class="p-6 bg-green-50 rounded-2xl border border-green-100">
                            <h4 class="font-bold text-green-700 text-3xl mb-2">木曜日 <span class="text-sm text-green-500 block mt-1">Thursday</span></h4>
                            <p class="text-sm text-slate-600">
                                <span class="font-bold">木 (Wood/Tree)</span>.
                                <br>Mnemonic: "Thor's Day" -> Thor protects the world tree? Or simply, Wood has 4 strokes -> 4th day.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
    """
    return culture_html

def main():
    vocab_data = [
        {"word": "トイレ", "kana": "といれ", "type": "①", "meaning": "Toilet", "category": "外来语", "structure": "Toilet", "etymology": "English 'Toilet'", "mnemonic": "发音像 'Toy-let' -> 玩具让给你！", "usage": "トイレはどこですか。"},
        {"word": "お手洗い", "kana": "おてあらい", "type": "③", "meaning": "Restroom", "category": "汉字词", "structure": "御(O)+手(Te)+洗(Arai)", "etymology": "Polite form. O (Honorable) + Hand + Wash.", "mnemonic": "洗手的地方 -> 也就是厕所的雅称。", "usage": "お手洗いに行きたいです。"},
        {"word": "隣", "kana": "となり", "type": "⓪", "meaning": "Next to / Neighbor", "category": "汉字词", "structure": "隣", "etymology": "Native word.", "mnemonic": "To-na-ri (偷那里) -> 小偷去偷隔壁邻居家！(from text)", "usage": "隣の部屋誰ですか。"},
        {"word": "周辺", "kana": "しゅうへん", "type": "⓪", "meaning": "Surroundings", "category": "汉字词", "structure": "周(Shu) + 边(Hen)", "etymology": "Chinese origin.", "mnemonic": "Shu-hen -> 书很多 -> 周边书店很多！", "usage": "駅の周辺は便利です。"},
        {"word": "今日", "kana": "きょう", "type": "①", "meaning": "Today", "category": "汉字词", "structure": "今(Kyo) + 日(U)", "etymology": "Native reading blend.", "mnemonic": "Kyou -> Q (Cute) -> 今天很 Cute！", "usage": "今日は水曜日です。"},
        {"word": "水曜日", "kana": "すいようび", "type": "③", "meaning": "Wednesday", "category": "汉字词", "structure": "水(Sui) + 曜日(Youbi)", "etymology": "Planet Mercury (Water Star).", "mnemonic": "三点水 -> 星期三！(from text)", "usage": "水曜日にテストがあります。"},
        {"word": "木曜日", "kana": "もくようび", "type": "③", "meaning": "Thursday", "category": "汉字词", "structure": "木(Moku) + 曜日(Youbi)", "etymology": "Planet Jupiter (Wood Star).", "mnemonic": "木字四笔划 -> 星期四！(from text)", "usage": "木曜日は休みです。"},
        {"word": "いくら", "kana": "いくら", "type": "①", "meaning": "How much", "category": "疑问词", "structure": "Ikura", "etymology": "Native word.", "mnemonic": "Ikura -> 一库拉 -> 一仓库拉走要多少钱？", "usage": "これはいくらですか。"},
        {"word": "こちら", "kana": "こちら", "type": "⓪", "meaning": "Here / This way (Polite)", "category": "指示词", "structure": "Ko + chira", "etymology": "Polite equivalent of Koko.", "mnemonic": "Co-chi-ra -> 口气啦 -> 语气很礼貌！", "usage": "こちらへどうぞ。"},
        {"word": "そちら", "kana": "そちら", "type": "⓪", "meaning": "There / That way (Polite)", "category": "指示词", "structure": "So + chira", "etymology": "Polite equivalent of Soko.", "mnemonic": "So-chi-ra.", "usage": "そちらは学校ですか。"},
        {"word": "あちら", "kana": "あちら", "type": "⓪", "meaning": "Over there (Polite)", "category": "指示词", "structure": "A + chira", "etymology": "Polite equivalent of Asoko.", "mnemonic": "A-chi-ra.", "usage": "あちらが入口です。"},
        {"word": "どちら", "kana": "どちら", "type": "①", "meaning": "Where / Which (Polite)", "category": "疑问词", "structure": "Do + chira", "etymology": "Polite equivalent of Doko.", "mnemonic": "Do-chi-ra.", "usage": "出身はどちらですか。"},
    ]

    vocab_content = generate_vocab_html(vocab_data)
    grammar_content = generate_grammar_html()
    culture_content = generate_culture_html()

    full_html = f"""
    <!-- VOCAB START -->
    {vocab_content}
    <!-- VOCAB END -->

    <!-- GRAMMAR START -->
    {grammar_content}
    <!-- GRAMMAR END -->

    <!-- CULTURE START -->
    {culture_content}
    <!-- CULTURE END -->
    """

    with open("/Users/hardentie/Downloads/vscode/learning/japanese/lesson3_supplements.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    
    print("Successfully generated lesson3_supplements.html")

if __name__ == "__main__":
    main()
