
import os

TARGET_FILE = "chapter2_lesson2.html"
TEST_DATA_FILE = "lesson2_test_data.js"

EXAM_TAB_BUTTON = """
            <button onclick="switchTab('exam')" id="tab-exam"
                class="tab-btn px-6 py-3 rounded-xl font-bold text-slate-600 hover:bg-white/600 whitespace-nowrap">
                📝 Exam (試験)
            </button>
"""

EXAM_SECTION_HTML = """
        <!-- 6. Exam Section -->
        <div id="content-exam" class="hidden space-y-8">
            <div class="glass-panel p-8 text-center">
                <h2 class="text-3xl font-black text-slate-800 mb-4">JLPT N5 Practice Test</h2>
                <p class="text-slate-600 mb-8">Test your mastery of Lesson 2 vocabulary and grammar.</p>
                
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <div class="p-4 bg-indigo-50 rounded-xl">
                        <div class="text-2xl font-bold text-indigo-600">30</div>
                        <div class="text-xs text-slate-500">Vocabulary</div>
                    </div>
                    <div class="p-4 bg-emerald-50 rounded-xl">
                        <div class="text-2xl font-bold text-emerald-600">30</div>
                        <div class="text-xs text-slate-500">Grammar</div>
                    </div>
                    <div class="p-4 bg-amber-50 rounded-xl">
                        <div class="text-2xl font-bold text-amber-600">20</div>
                        <div class="text-xs text-slate-500">Context</div>
                    </div>
                    <div class="p-4 bg-pink-50 rounded-xl">
                        <div class="text-2xl font-bold text-pink-600">20</div>
                        <div class="text-xs text-slate-500">Listening</div>
                    </div>
                </div>

                <button onclick="startExam()" class="px-8 py-4 bg-indigo-600 text-white font-bold rounded-xl shadow-lg hover:bg-indigo-700 transition transform hover:scale-105">
                    Start Exam
                </button>
            </div>

            <!-- Quiz Container (Hidden initially) -->
            <div id="quiz-container" class="hidden space-y-6">
                <!-- Progress Bar -->
                <div class="w-full bg-slate-200 rounded-full h-2.5">
                    <div id="quiz-progress" class="bg-indigo-600 h-2.5 rounded-full" style="width: 0%"></div>
                </div>
                
                <!-- Question Card -->
                <div class="glass-panel p-8">
                    <div class="flex justify-between items-center mb-6">
                        <span id="question-tag" class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-bold uppercase tracking-wider">VOCAB</span>
                        <span id="question-counter" class="text-slate-400 font-mono text-sm">1/100</span>
                    </div>
                    
                    <h3 id="question-text" class="text-2xl font-bold text-slate-800 mb-8 leading-relaxed">Question text...</h3>
                    
                    <div id="options-grid" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- Options injected here -->
                    </div>
                    
                    <!-- Feedback -->
                    <div id="feedback-area" class="hidden mt-6 p-4 rounded-xl">
                        <p id="feedback-text" class="font-bold"></p>
                        <p id="feedback-explanation" class="text-sm mt-2"></p>
                    </div>
                </div>
                
                <!-- Controls -->
                <div class="flex justify-between">
                    <button onclick="quitExam()" class="text-slate-400 hover:text-red-500 font-bold px-4">Quit</button>
                    <button id="next-btn" onclick="nextQuestion()" class="hidden px-6 py-3 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition shadow-lg">
                        Next Question →
                    </button>
                </div>
            </div>

            <!-- Results (Hidden) -->
            <div id="quiz-results" class="hidden text-center glass-panel p-12">
                <div class="w-24 h-24 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-6 text-4xl">
                    🏆
                </div>
                <h2 class="text-3xl font-bold text-slate-800 mb-2">Exam Complete!</h2>
                <p class="text-slate-500 mb-8">Here is your performance report</p>
                
                <div class="text-6xl font-black text-indigo-600 mb-8" id="final-score">85%</div>
                
                <div class="grid grid-cols-2 gap-4 max-w-md mx-auto mb-8">
                    <div class="p-4 bg-white rounded-xl border border-slate-100">
                        <div class="text-sm text-slate-500">Correct</div>
                        <div class="text-xl font-bold text-emerald-600" id="result-correct">85</div>
                    </div>
                    <div class="p-4 bg-white rounded-xl border border-slate-100">
                        <div class="text-sm text-slate-500">Wrong</div>
                        <div class="text-xl font-bold text-red-500" id="result-wrong">15</div>
                    </div>
                </div>
                
                <button onclick="location.reload()" class="px-8 py-3 bg-slate-800 text-white font-bold rounded-xl hover:bg-slate-700 transition">
                    Back to Lesson
                </button>
            </div>
        </div>
"""

QUIZ_ENGINE_SCRIPT = """
    <script>
        // Quiz Engine
        let currentQuestions = [];
        let currentQuestionIndex = 0;
        let score = 0;
        let isExamActive = false;

        function startExam() {
            // Flatten questions
            // LESSON2_TEST_DATA is defined in injected script
            if (typeof LESSON2_TEST_DATA === 'undefined') {
                alert("Error: Test data not loaded.");
                return;
            }
            
            const q = LESSON2_TEST_DATA;
            currentQuestions = [
                ...q.vocabulary,
                ...q.grammar,
                ...q.context,
                ...q.listening
            ];
            
            // Shuffle full deck? Or keep sections? Let's shuffle for variety exam feel
            // Fisher-Yates shuffle
            for (let i = currentQuestions.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [currentQuestions[i], currentQuestions[j]] = [currentQuestions[j], currentQuestions[i]];
            }

            currentQuestionIndex = 0;
            score = 0;
            isExamActive = true;
            
            // UI Update
            document.querySelector('.glass-panel.text-center').classList.add('hidden'); // Hide start screen
            document.getElementById('quiz-container').classList.remove('hidden');
            
            loadQuestion();
        }

        function loadQuestion() {
            if (currentQuestionIndex >= currentQuestions.length) {
                showResults();
                return;
            }

            const q = currentQuestions[currentQuestionIndex];
            
            // Update UI
            document.getElementById('question-counter').innerText = `${currentQuestionIndex + 1}/${currentQuestions.length}`;
            document.getElementById('question-tag').innerText = q.type.split('_')[0].toUpperCase();
            document.getElementById('question-text').innerHTML = q.question;
            
            // Progress
            const pct = ((currentQuestionIndex) / currentQuestions.length) * 100;
            document.getElementById('quiz-progress').style.width = `${pct}%`;
            
            // Reset state
            document.getElementById('feedback-area').classList.add('hidden');
            document.getElementById('next-btn').classList.add('hidden');
            
            const optionsGrid = document.getElementById('options-grid');
            optionsGrid.innerHTML = '';
            
            q.options.forEach(opt => {
                const btn = document.createElement('button');
                btn.className = 'p-6 text-left rounded-xl border-2 border-slate-100 hover:border-indigo-200 hover:bg-indigo-50 transition font-medium text-slate-700 text-lg group';
                btn.onclick = () => checkAnswer(opt, q, btn);
                btn.innerHTML = `<span class="inline-block w-8 h-8 rounded-lg bg-slate-100 text-slate-500 text-sm font-bold flex items-center justify-center mr-3 group-hover:bg-indigo-200 group-hover:text-indigo-700 transition">?</span> ${opt}`;
                optionsGrid.appendChild(btn);
            });
        }

        function checkAnswer(selected, question, btnElement) {
            // Disable all buttons
            const buttons = document.querySelectorAll('#options-grid button');
            buttons.forEach(b => b.disabled = true);
            
            const isCorrect = selected === question.answer;
            
            if (isCorrect) {
                score++;
                btnElement.classList.remove('border-slate-100', 'hover:border-indigo-200', 'hover:bg-indigo-50');
                btnElement.classList.add('border-emerald-500', 'bg-emerald-50', 'text-emerald-700');
                btnElement.querySelector('span').classList.add('bg-emerald-200', 'text-emerald-800');
                btnElement.querySelector('span').innerText = '✓';
                playSound('correct');
            } else {
                btnElement.classList.remove('border-slate-100', 'hover:border-indigo-200', 'hover:bg-indigo-50');
                btnElement.classList.add('border-red-500', 'bg-red-50', 'text-red-700');
                btnElement.querySelector('span').classList.add('bg-red-200', 'text-red-800');
                btnElement.querySelector('span').innerText = '✗';
                
                // Highlight correct
                buttons.forEach(b => {
                    if (b.innerText.includes(question.answer)) { // Simple check, might be risky with substrings
                        // Better to check data-val if we stored it, but clean text match usually works
                         b.classList.add('border-emerald-500', 'bg-emerald-50');
                    }
                });
                playSound('wrong');
            }
            
            // Show Feedback
            const fb = document.getElementById('feedback-area');
            fb.classList.remove('hidden', 'bg-emerald-100', 'text-emerald-800', 'bg-red-100', 'text-red-800');
            fb.classList.add(isCorrect ? 'bg-emerald-100' : 'bg-red-100', isCorrect ? 'text-emerald-800' : 'text-red-800');
            
            document.getElementById('feedback-text').innerText = isCorrect ? 'Correct! Excellent.' : 'Incorrect.';
            document.getElementById('feedback-explanation').innerText = question.explanation || "";
            
            document.getElementById('next-btn').classList.remove('hidden');
        }

        function nextQuestion() {
            currentQuestionIndex++;
            loadQuestion();
        }

        function showResults() {
            document.getElementById('quiz-container').classList.add('hidden');
            document.getElementById('quiz-results').classList.remove('hidden');
            
            const percentage = Math.round((score / currentQuestions.length) * 100);
            document.getElementById('final-score').innerText = `${percentage}%`;
            document.getElementById('result-correct').innerText = score;
            document.getElementById('result-wrong').innerText = currentQuestions.length - score;
            
            // Simple sound
            if (percentage >= 80) playSound('victory');
        }

        function quitExam() {
            if(confirm("Exit exam? Progress will be lost.")) {
                 location.reload();
            }
        }
        
        function playSound(type) {
            // Optional: Implement simple beep or use Audio object if assets exist
        }
    </script>
"""

# Read Files
with open(TARGET_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

with open(TEST_DATA_FILE, 'r', encoding='utf-8') as f:
    test_data_js_content = f.read() # Actually this file is valid JS: "const LESSON2_... = ..."

# 1. Inject Exam Tab Button
if 'switchTab(\'exam\')' not in html:
    # Find the closing button of the tab bar
    # Look for the last tab button: 'practice'
    # <button onclick="switchTab('practice')" ... > ... </button>
    practice_btn_idx = html.find("switchTab('practice')")
    if practice_btn_idx != -1:
        # Find closing </button> for this button
        btn_close_idx = html.find("</button>", practice_btn_idx)
        if btn_close_idx != -1:
            insertion_point = btn_close_idx + 9
            html = html[:insertion_point] + EXAM_TAB_BUTTON + html[insertion_point:]
            print("Injected Exam Tab Button.")

# 2. Inject Exam Content Section
if 'id="content-exam"' not in html:
    # Insert after content-practice div
    # Find closing div of content-practice. This is hard without ID closing.
    # But usually sections are sequential.
    # Look for `<!-- 1. Vocabulary Section -->` or similar markers.
    # We can append it at the end of the `main` tag or before the specific script tag.
    
    # Or find <div id="content-practice"> ... (scan for matching closing div? No too hard regex)
    # Let's insert BEFORE the closing </main> tag.
    main_close = html.find("</main>")
    if main_close != -1:
        html = html[:main_close] + EXAM_SECTION_HTML + html[main_close:]
        print("Injected Exam Content Section.")

# 3. Inject Test Data Script
# We can inject it before the last script tag or body close
if 'const LESSON2_TEST_DATA' not in html:
    body_close = html.find("</body>")
    script_block = f"<script>\n{test_data_js_content}\n</script>\n"
    if body_close != -1:
        html = html[:body_close] + script_block + html[body_close:]
        print("Injected Test Data JS.")

# 4. Inject Quiz Engine
if 'function startExam()' not in html:
    body_close = html.find("</body>")
    if body_close != -1:
        html = html[:body_close] + QUIZ_ENGINE_SCRIPT + html[body_close:]
        print("Injected Quiz Engine.")

# 5. Update switchTab function to handle 'exam'
# Find: ['vocab', 'grammar', 'text', 'culture', 'practice'].forEach
# Replace with: ['vocab', 'grammar', 'text', 'culture', 'practice', 'exam'].forEach
if "'practice', 'exam'" not in html:
    html = html.replace("'practice'].forEach", "'practice', 'exam'].forEach")
    print("Updated switchTab function.")

# Write back
with open(TARGET_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("Injection complete.")
