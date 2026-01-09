# 📋 Lesson Metadata / Page Config
>
> **Maps to**: `<head>`, `<title>`, and Top Navigation

- **Lesson Number**: [e.g., 1]
- **Lesson Title**: [e.g., Introduction & Greetings]
- **Subtitle**: [e.g., First Encounters]
- **Page Title Tag**: `第[X]课：[Title] – 盾盾日语全覆盖笔记`
- **Audio Folder ID**: [e.g., lesson1] (All audio paths will leverage this: `assets/audio/[lessonID]/...`)

---

# 1. 📚 Vocabulary Section (`#content-vocab`)
>
> **Structure**: Grid Layout (`.grid-cols-4`) + Teacher's Corner
> **Audio Format**: `vocab_[word_romaji]`

## 1.1 Vocabulary Cards

| Kanji/Word | Kana (Reading) | Accent (0-3) | English Meaning | Audio Filename | Tags (Noun/Verb/etc.) | Etymology/Mnemonic (Details) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **わたし** | わたし | ⓪ | I, Me | `vocab_watashi` | Pronoun | "Watashi" sounds like "Wash", I wash myself. |
| **学生** | がくせい | ⓪ | Student | `vocab_gakusei` | Noun | **Gaku** (Study) + **Sei** (Life). |
| **中国** | ちゅうごく | ① | China | `vocab_chuugoku` | Place | Middle Kingdom. |

## 1.2 Teacher's Corner (`.bg-indigo-50`)
>
> **Title**: 👨‍🏫 老师的重点笔记

- **Note 1**: [Content about Pronouns usage...]
- **Note 2**: [Content about Pitch Accent importance...]

---

# 2. 🧠 Grammar Section (`#content-grammar`)
>
> **Structure**: Vertical Stack of `.glass-panel` blocks.
> **Audio Format**: `grammar_[pattern#]_[example#]`

## Pattern 01: [Pattern Name, e.g., N1 は N2 です]

- **Visual Structure Block**:
  - Element A: `N1`
  - Connector: `は (wa)`
  - Element B: `N2`
  - Ender: `です (desu)`
- **Explanation**: [Topic Marker 'Wa' indicates...]

### Examples

1. **Sentence**: 私は学生です。
   - **Translation**: I am a student.
   - **Highlight/Focus**: `は` marks the topic.
   - **Audio**: `grammar_1_1`

2. **Sentence**: 田中さんは会社員です。
   - **Translation**: Mr. Tanaka is an office worker.
   - **Audio**: `grammar_1_2`

## Pattern 02: [Pattern Name, e.g., N1 は N2 じゃありません]

...

---

# 3. 💬 Text / Dialogue Section (`#content-text`)
>
> **Structure**: Scenes inside `.glass-panel`. Chat Bubbles (Left/Right).
> **Audio Format**: `text_[scene#]_[line#]`

## Scene 01: [Title, e.g., 出会い (First Meeting)]
>
> **Background Style**: `bg-indigo-500` badge

- **Line 1 (Left - Speaker A)**:
  - **Speaker Image**: [e.g., Li.png]
  - **Japanese**: JC企画の小野さんですか。
  - **English**: Is this Ms. Ono from JC Kikaku?
  - **Audio**: `text_1_1`

- **Line 2 (Right - Speaker B)**:
  - **Speaker Image**: [e.g., Ono.png]
  - **Japanese**: はい、小野です。李さんですか。
  - **English**: Yes, I'm Ono. Are you Mr. Li?
  - **Audio**: `text_1_2`

## Scene 02: [Title]

...

---

# 4. 🌸 Culture Section (`#content-culture`)
>
> **Structure**: `.glass-panel` cards with icons.

## Card 1: [Title, e.g., The Concept of Uchi-Soto]

- **Icon**: 🏠
- **Subtitle**: The Core of Japanese Social Harmony
- **Main Text**:
  In Japan, language changes based on who you are talking to...
- **Visual/List Items**:
  - **Uchi (Inside)**: Family, Company. Rule: Be Humble.
  - **Soto (Outside)**: Clients, Strangers. Rule: Be Respectful.

## Card 2: [Title, e.g., Business Cards (Meishi)]

- **Icon**: 📇
- **Content**: ...

---

# 5. ✍️ Practice Section (`#content-practice`)
>
> **Structure**: `.practice-item` blocks with Javascript checking logic.
> **Audio**: None (usually).

## Drill 01: Substitution (Title: 替换练习)
>
> **Badge**: `TYPE 01` (Indigo)
> **Instruction**: Replace A and B.

- **Example**: A / B → AはBです。
- **Questions**:
  1. **Prompt**: 森 / 学生
     - **Inputs**: `[Input Field]`
     - **Correct Answers**: `森さんは学生です`, `森さんは学生です。` (Support multiple formats sep by `/`)

## Drill 02: Negation (Title: 否定变换)
>
> **Badge**: `TYPE 02` (Rose)
> **Instruction**: Change to negative form.

- **Questions**:
  1. **Prompt**: 田中さんは中国人です。
     - **Correct Answers**: `田中さんは中国人じゃありません`

## Drill Final: Comprehensive Challenge
>
> **Badge**: `30 Questions` (Gold)
> **Structure**: Mixed input types (Particles, Vocab Matching, Translation).

- **Q1 (Particles)**: 私 `[Input]` 中国人です。 -> Answer: `は`
- **Q2 (Translation)**: I am Li. -> Answer: `私は李です`
...
