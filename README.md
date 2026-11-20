# BUDDY & KITTY — A Living, Interactive AI Digital Pet Game

A living, fully interactive virtual digital pet game featuring **Buddy** the dog and **Kitty** the cat. Unlike static pet mockups, Buddy and Kitty are engineered with **layered SVG character rigs** with independently controllable body parts, a JavaScript animation state machine, gradual 5-stage growth, procedural Web Audio sound synthesis, and a bilingual command personality engine supporting English and Bengali!

---

## 🌟 Key Highlights & Features

### 1. Living Layered Character Rig
- **Independently Controllable Body Parts**: Separate head, torso, belly, ears, eyebrows, eyelids, pupils, muzzle, mouth, front legs/paws, back legs, and tail.
- **Natural Idle Animation**:
  - Continuous sinusoidal breathing (torso expansion and head bobbing)
  - Varied randomized eye blinking (every 2.5–5s) with realistic eyelid arcs
  - Looking around with drifting pupils and eye highlights
  - Ear twitching and continuous tail wagging
  - Interactive petting: click or stroke the pet to make them purr/bark and smile with floating hearts!
- **Interactive Animations**:
  - **Walking**: Alternating front and back leg cycles with vertical body bobbing, tail counter-balance, and stage boundary turnaround.
  - **Eating**: Food dish appears on stage, pet turns and approaches, mouth visibly opens, chews food over 4 chewing cycles with crumb bursts and sound, swallows with a happy grin, and thanks the user.
  - **Dancing**: 150 BPM full-body dance routine with arms/paws waving up and down, legs stepping in groove, head/ears rocking, tail wagging, upbeat procedural chiptune melody, and a triumphant celebration pose!
  - **Sleeping & Waking**: Stage lights smoothly dim into night sky with stars, pet curls into resting pose, eyelids shut tight, gentle slow breathing, floating "Zzz" letters, and a waking sequence with front paws stretching forward and a big yawn!

### 2. Real 5-Stage Pet Growth System
The pet visibly grows in size and changes proportions over time through regular care:
1. **Stage 1: Baby** (0.72x scale, cute chibi puppy/kitten proportions)
2. **Stage 2: Little Pet** (0.85x scale, playful toddler)
3. **Stage 3: Growing Pet** (0.98x scale, developing companion)
4. **Stage 4: Young Pet** (1.10x scale, silver bell medal accessory)
5. **Stage 5: Fully Grown Pet** (1.22x scale, majestic adult with golden star crown accessory)

- **Gradual Evolution**: Feeding grants Growth Progress (+5 to +15 pts per meal).
- **Celebration Ceremony**: Reaching 100% growth triggers an evolution ceremony with confetti, fanfare, and an achievement banner!
- **Bond XP & Levels**: Interacting, playing, and chatting rewards XP to level up your bond.
- **Full Persistence**: Growth stage, level, and stats persist across reloads in `localStorage` and backend `pet_save.json`.

### 3. Interactive Personality (English & Bengali)
- **Natural Command-to-Action Intent Mapping**:
  - Saying *"Let's dance"*, *"Can you dance?"*, or *"নাচো"* / *"ড্যান্স করো"* immediately triggers the dance routine!
  - Saying *"Are you hungry?"*, *"Feed me"*, or *"খাবার খাও"* / *"ক্ষিদে পেয়েছে"* offers food and feeds the pet!
  - Saying *"Let's play"* or *"খেলা করো"* triggers ball play!
  - Saying *"Good night"* or *"ঘুমাও"* puts the pet to bed!
  - Saying *"Good morning"* or *"জেগে ওঠো"* wakes the pet up!
  - Asking *"How are you?"* or *"কেমন আছো?"* inspects real hunger, happiness, and energy stats!
- **External AI Integration**: Optional proxy to OpenAI-compatible LLMs via `server.py` with seamless offline local fallback.

### 4. Zero-Dependency Procedural Audio Engine
- Built with standard browser **Web Audio API**:
  - Procedural eating crunch and chewing sound
  - Cheerful upward arpeggio chime
  - Cute footsteps
  - Upbeat dance music loop
  - Soft lullaby ambient sleep chords
  - Level-up / evolution fanfare
- UI master volume slider and one-click Mute/Unmute toggle.

---

## 🚀 Quick Start (Windows)

### Method A: One-Click Launcher (Recommended)
1. Double-click **`RUN_APP.bat`**.
2. The game will automatically start the local server and open `http://localhost:8000` in your default browser.

### Method B: Manual Python Command
```powershell
python server.py
```
Then navigate to `http://localhost:8000`.

### Method C: Direct Browser Opening (No Server Required)
Simply double-click `index.html` to run the game in any modern browser (Chrome, Edge, Firefox).

---

## 🔍 File Verification

Run `CHECK_FILES.bat` to verify that all project files are present and properly organized:
```cmd
CHECK_FILES.bat
```
All files will report `[OK]`.

---

## ⚙️ AI Conversation Configuration (Optional)

To enable external AI-powered dialogue:
1. Copy `.env.example` to `.env`:
   ```cmd
   copy .env.example .env
   ```
2. Open `.env` and fill in your API credentials:
   ```env
   OPENAI_API_KEY=your_actual_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1
   AI_MODEL=gpt-4o-mini
   PORT=8000
   ```
3. Restart `server.py` or double-click `RUN_APP.bat`.
*(If no API key is set, the pet automatically uses its built-in local personality engine!)*

---

## 📁 Project Architecture

```
buddy-and-kitty/
├── index.html            # Main game layout with responsive stage and chat
├── style.css             # Modern Tailwind-compatible styling, animations, stage themes
├── manifest.json         # Progressive Web App manifest
├── sw.js                 # Service worker for offline caching
├── icon.svg              # Scalable paw logo
├── icon.png              # App icon
├── server.py             # Python HTTP server & safe API proxy
├── RUN_APP.bat           # Windows launcher
├── CHECK_FILES.bat       # File verification script
├── README.md             # Project documentation
├── TEST_REPORT.md        # Comprehensive testing and verification report
├── .env.example          # Sample environment configuration
├── assets/
│   ├── buddy.svg         # Standalone Buddy SVG asset
│   └── kitty.svg         # Standalone Kitty SVG asset
├── icons/
│   ├── icon-192.svg      # PWA 192x192 icon
│   ├── icon-512.svg      # PWA 512x512 icon
│   └── maskable-512.svg  # PWA maskable icon
└── js/
    ├── pet-model.js      # Stats, 5 growth stages, XP, cooldowns, save/load
    ├── pet-renderer.js   # Layered SVG character renderer with independent parts
    ├── pet-animator.js   # Animation state machine (Idle, Walk, Eat, Dance, Sleep, etc.)
    ├── audio.js          # Web Audio procedural sound synthesizer
    ├── personality.js    # Bilingual intent recognition & dialogue
    └── app.js            # Main application coordinator
```
