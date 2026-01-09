
import os

def inject_test_section():
    base_dir = '/Users/hardentie/Downloads/vscode/learning/japanese'
    target_path = os.path.join(base_dir, 'chapter2_lesson3.html')
    data_path = os.path.join(base_dir, 'lesson3_test_data.js')
    
    with open(target_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    with open(data_path, 'r', encoding='utf-8') as f:
        js_data = f.read()

    # 1. Inject Navigation Tab
    # Look for the last tab button, e.g., 'Practice'
    # <button onclick="switchTab('practice')" ...>Practice</button>
    # We want to add 'Exam' after it.
    
    practice_tab_marker = "switchTab('practice')"
    
    if practice_tab_marker in html:
        # Find the closing tag of the practice button </button>
        # This is a bit risky with string replacement if lines vary.
        # Let's verify the context.
        pass
    else:
        print("Error: Practice tab not found.")
        return

    # Construct the Exam Tab Button
    exam_tab_html = """
                <button onclick="switchTab('exam')" id="tab-exam" class="tab-btn px-6 py-2 rounded-full text-slate-500 font-bold hover:bg-white/50">
                    Exam (試験)
                </button>
    """
    
    # Insert after Practice Tab
    # We replace the practice button with Practice Button + Exam Button
    # Need to regex or find the full string of the practice button?
    # Or just find `switchTab('practice')` and append after the next `</button>`.
    
    idx_practice = html.find("switchTab('practice')")
    idx_btn_end = html.find("</button>", idx_practice) + 9 
    
    # Check if we already injected
    if "switchTab('exam')" not in html:
        html = html[:idx_btn_end] + "\n" + exam_tab_html + html[idx_btn_end:]
        print("Injected Exam Tab.")
    else:
        print("Exam Tab already exists.")

    # 2. Inject Content Section
    # We need to add <div id="content-exam">...</div>
    # It should go after <div id="content-practice">...</div>
    # Practice section ends... where?
    # We can search for the END of the container that holds all content-divs?
    # Or just append after content-practice.
    
    practice_div_start = '<div id="content-practice"'
    
    # Define the Exam UI HTML
    exam_content_html = """
        <!-- 6. Exam Section -->
        <div id="content-exam" class="hidden space-y-8">
            <div class="glass-panel p-8">
                <div class="flex items-center justify-between mb-8">
                    <h2 class="text-3xl font-black text-slate-800">JLPT N5 Practice Test</h2>
                    <span class="bg-indigo-100 text-indigo-700 px-4 py-1 rounded-full text-sm font-bold">100 Questions</span>
                </div>
                
                <div id="exam-start-screen" class="text-center py-12">
                    <div class="text-6xl mb-6">📝</div>
                    <h3 class="text-2xl font-bold text-slate-700 mb-4">Ready to test your knowledge?</h3>
                    <p class="text-slate-500 mb-8 max-w-md mx-auto">This test covers Vocabulary, Grammar, Context, and Math from Lesson 3. Recommended time: 20 minutes.</p>
                    <button onclick="startExam()" class="bg-indigo-600 text-white px-8 py-3 rounded-xl font-bold shadow-lg hover:bg-indigo-700 transition transform hover:scale-105">
                        Start Exam
                    </button>
                </div>

                <div id="exam-ui" class="hidden">
                    <div class="mb-6 flex justify-between items-center bg-slate-100 p-4 rounded-xl">
                        <div class="flex items-center gap-4">
                            <span class="font-mono font-bold text-indigo-600 text-xl" id="q-counter">Q1/100</span>
                            <span class="text-xs text-slate-400 uppercase tracking-wider font-bold" id="q-category">VOCABULARY</span>
                        </div>
                        <div class="h-2 w-48 bg-slate-200 rounded-full overflow-hidden">
                            <div id="q-progress" class="h-full bg-indigo-500 w-0 transition-all duration-300"></div>
                        </div>
                    </div>

                    <div class="mb-8">
                        <p class="text-2xl font-bold text-slate-800 mb-2" id="q-text">Question goes here?</p>
                        <p class="text-slate-500 text-sm italic" id="q-type">Type: Particle</p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8" id="q-options">
                        <!-- Options injected here -->
                    </div>

                    <div id="q-feedback" class="hidden p-4 rounded-xl bg-slate-50 border border-slate-100 mb-4">
                        <p class="font-bold mb-1" id="feedback-title">Correct!</p>
                        <p class="text-slate-600 text-sm" id="feedback-reason">Explanation...</p>
                        <button onclick="nextQuestion()" class="mt-4 bg-indigo-100 text-indigo-700 px-6 py-2 rounded-lg font-bold hover:bg-indigo-200">Next Question →</button>
                    </div>
                </div>

                <div id="exam-results" class="hidden text-center py-12">
                    <div class="text-6xl mb-6">🏆</div>
                    <h3 class="text-3xl font-bold text-slate-800 mb-2">Test Complete!</h3>
                    <p class="text-xl text-slate-600 mb-8">You scored: <span class="font-black text-indigo-600 text-4xl" id="final-score">85</span>/100</p>
                    <div class="grid grid-cols-4 gap-4 max-w-2xl mx-auto mb-8 text-sm">
                         <div class="p-3 bg-slate-50 rounded-lg"><div class="font-bold text-slate-400">Vocab</div><div class="font-black text-lg" id="score-vocab">0/30</div></div>
                         <div class="p-3 bg-slate-50 rounded-lg"><div class="font-bold text-slate-400">Grammar</div><div class="font-black text-lg" id="score-grammar">0/30</div></div>
                         <div class="p-3 bg-slate-50 rounded-lg"><div class="font-bold text-slate-400">Context</div><div class="font-black text-lg" id="score-context">0/20</div></div>
                         <div class="p-3 bg-slate-50 rounded-lg"><div class="font-bold text-slate-400">Numbers</div><div class="font-black text-lg" id="score-math">0/20</div></div>
                    </div>
                    <button onclick="location.reload()" class="text-slate-500 underline hover:text-indigo-600">Restart Lesson</button>
                </div>
            </div>
        </div>
    """
    
    if 'id="content-exam"' not in html:
        # Find where to insert. Before the script tags usually?
        # Or after #content-practice closing div.
        # Let's look for the comment <!-- 5. Practice Section --> to identify the block.
        # But we need the END of it.
        # Finding the layout main container close might be easiest.
        
        # Let's search for the script block start, and insert before it.
        idx_script = html.find("<script>")
        # A bit risky if there are scripts in head.
        # Let's verify content-practice structure.
        # It's inside a container...
        # Let's append to the end of the `container mx-auto custom-scrollbar` block?
        
        # Safer: Find `<!-- 5. Practice Section -->`
        mark_practice = '<!-- 5. Practice Section -->'
        if mark_practice in html:
            # We want to be AFTER this section.
            # This section starts a div. We need to find its matching closing div.
            # This is hard without parsing.
            
            # ALTERNATIVE: Insert before the footer or body close?
            # Looking at file:
            # </div> <!-- End of content container -->
            # <script>
            
            # Let's find the last `</div>` before `<script>`?
            # Or just insert before `<script>` logic for tabs.
            
            # Let's use `content-practice` as a locator, find the next `class="hidden..."` div?
            # Practice section is `id="content-practice"`.
            # We can find `id="content-practice"` block.
            # It's a `<div ...>`
            # Inserting `exam_content_html` *after* the `content-practice` DIV opening is NOT what we want. We want it as a sibling.
            
            # Strategy:
            # Find `id="content-practice"`
            # Replace `id="content-practice" ... >` with `id="content-practice" ... > ... </div>` + exam_html? No.
            
            # Let's look for where the TAB LOGIC script helps us.
            # Script has `const tabs = ['vocab', 'grammar', 'text', 'culture', 'practice', 'exam'];` (We need to update this too!)
            
            # Let's just insert it at the very end of the content area.
            # Searching for the last `</div>` inside the wrapper?
            # Let's scan for `<script>` at the bottom of the body.
            # Insert before `<script>`.
            
            pass # Logic inside write block
            html_parts = html.split('<script>')
            # usually the last script block is the main logic.
            # html_parts[-1] is the script content + </body></html>
            # So insert before html_parts[-1] (or -2 if multiple scripts)
            
            # Let's assume the main script tag is unique enough or last one.
            last_script_idx = html.rfind("<script>")
            html = html[:last_script_idx] + exam_content_html + "\n" + html[last_script_idx:]
            print("Injected Exam Content Section.")
    
    # 3. Inject Quiz Logic
    # We need to add the JS data and the engine.
    
    quiz_engine_js = """
    // --- EXAM ENGINE ---
    let currentQIndex = 0;
    let score = 0;
    let categoryScores = { "Vocabulary": 0, "Grammar": 0, "Context": 0, "Numbers": 0 };
    
    function startExam() {
        document.getElementById('exam-start-screen').classList.add('hidden');
        document.getElementById('exam-ui').classList.remove('hidden');
        currentQIndex = 0;
        score = 0;
        // Reset category scores
        for (let k in categoryScores) categoryScores[k] = 0;
        loadQuestion();
    }
    
    function loadQuestion() {
        const q = lesson3QuizData[currentQIndex];
        document.getElementById('q-counter').innerText = `Q${currentQIndex + 1}/${lesson3QuizData.length}`;
        document.getElementById('q-progress').style.width = `${((currentQIndex) / lesson3QuizData.length) * 100}%`;
        
        document.getElementById('q-text').innerText = q.question;
        document.getElementById('q-category').innerText = q.category;
        document.getElementById('q-type').innerText = `Type: ${q.type}`;
        
        const optsContainer = document.getElementById('q-options');
        optsContainer.innerHTML = '';
        
        // Hide feedback
        document.getElementById('q-feedback').classList.add('hidden');
        
        q.options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = "p-4 bg-white border border-slate-200 rounded-xl hover:border-indigo-400 hover:bg-indigo-50 font-bold text-left transition";
            btn.innerText = opt;
            btn.onclick = () => checkAnswer(opt, q);
            optsContainer.appendChild(btn);
        });
    }
    
    function checkAnswer(selected, q) {
        const isCorrect = selected === q.answer;
        const feedback = document.getElementById('q-feedback');
        const title = document.getElementById('feedback-title');
        const reason = document.getElementById('feedback-reason');
        
        feedback.classList.remove('hidden');
        
        if (isCorrect) {
            score++;
            if (categoryScores[q.category] !== undefined) categoryScores[q.category]++;
            title.innerText = "✅ Correct!";
            title.className = "font-bold text-green-600 mb-1";
            feedback.className = "p-4 rounded-xl bg-green-50 border border-green-100 mb-4";
        } else {
            title.innerText = "❌ Incorrect";
            title.className = "font-bold text-red-600 mb-1";
            feedback.className = "p-4 rounded-xl bg-red-50 border border-red-100 mb-4";
        }
        
        reason.innerText = `${q.explanation} (Answer: ${q.answer})`;
        
        // Disable buttons
        const btns = document.getElementById('q-options').children;
        for (let btn of btns) {
            btn.disabled = true;
            if (btn.innerText === q.answer) btn.classList.add('bg-green-100', 'border-green-400');
            else if (btn.innerText === selected && !isCorrect) btn.classList.add('bg-red-100', 'border-red-400');
            else btn.classList.add('opacity-50');
        }
    }
    
    function nextQuestion() {
        currentQIndex++;
        if (currentQIndex < lesson3QuizData.length) {
            loadQuestion();
        } else {
            showResults();
        }
    }
    
    function showResults() {
        document.getElementById('exam-ui').classList.add('hidden');
        document.getElementById('exam-results').classList.remove('hidden');
        
        document.getElementById('final-score').innerText = score;
        
        // Update breakdown
        document.getElementById('score-vocab').innerText = `${categoryScores['Vocabulary']}/30`; // Approx
        document.getElementById('score-grammar').innerText = `${categoryScores['Grammar']}/30`;
        document.getElementById('score-context').innerText = `${categoryScores['Context']}/20`;
        document.getElementById('score-math').innerText = `${categoryScores['Numbers']}/20`;
    }
    """
    
    # Append JS data + Engine to the existing script block
    # We find the last `</script>` and insert before it?
    # Or start a new script block at the end.
    
    combined_script = f"""
    <script>
    {js_data}
    {quiz_engine_js}
    
    // Update Tab Switching Logic to include 'exam'
    // This is a hacky override if the original function uses a hardcoded list.
    // If original is `const tabs = [...]`, we might need to redefine it or push to it if it's global.
    // Let's inspect the file later to see if `tabs` is global.
    // Assuming we can just append, but we should check.
    </script>
    """
    
    # Append to body end
    html = html.replace('</body>', f'{combined_script}</body>')
    print("Injected Quiz Logic.")
    
    # 4. Update Tab List in JS
    # If there is a `const tabs = [...]` line, we need to add 'exam'.
    if "const tabs =" in html:
        # crude replace
        html = html.replace("'practice']", "'practice', 'exam']")
        print("Updated tabs array.")
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    inject_test_section()
