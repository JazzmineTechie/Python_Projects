# 🐍 Python Portfolio: Demo & Real-World Projects

Welcome to my Python project repository! This space serves as a central hub for my Python portfolio, showcasing a mix of practical, real-world applications and deep-dive technical demonstrations. 

Each project highlights different core skills, from data manipulation and automation to software engineering best practices.

---

## 🚀 Featured Projects

### 🧽 1. Automated Excel Data Cleaner
*   **Directory:** `/cleaner`
*   **Type:** Real-World Utility
*   **Key Tech:** `pandas`, `openpyxl`, `Python 3`
*   **Description:** A script that automates the tedious parts of data cleaning. It eliminates duplicate entries, removes blank rows/columns, standardizes column headers, and trims accidental whitespace from text data.
*   **Impact:** Saves hours of manual data preparation, formatting raw data into a reliable, analysis-ready structure in seconds.

---

## 🛠️ Core Skills Demonstrated

*   **Data Processing:** Cleansing, reshaping, and engineering datasets.
*   **Automation:** Replacing repetitive manual spreadsheet workflows with efficient scripts.
*   **Code Quality:** Writing clean, modular, and readable Python code following PEP 8.
*   **Environment Management:** Keeping dependencies isolated and documented.

---


### 📁 2. Matcha Studio
*   **Directory:** `/matchastudio`
*   **Type:** Demo
*   **Key Tech:** `pygame, numpy, pyinstaller`
*   **Description:** A demo game using only python libraries that involves creating music using a keyboard, bass guitar and drum, using sounds created from python itself.  It uses Pygame's built-in mathematical sound synthesizer (pygame.sndarray), meaning you do not need to download any external .wav or .mp3 audio files. The code generates real musical frequencies on the fly for the Piano, Drums, and Bass Guitar!


---

## 🛠️ Core Skills Demonstrated

*   **Object-Oriented Programming (OOP):** Instead of writing copy-pasted code for 7 different rectangles, I built a single PianoKey class template. The for i in range(7): loop runs 7 times, passing unique coordinates into the template to generate 7 independent objects in memory.
*   **State Management:** (self.is_pressed): Variables that keep track of a status are called flags or states. When MOUSEBUTTONDOWN happens inside a key, its state changes to True. When MOUSEBUTTONUP happens anywhere, all states reset to False. The code looks at this state 60 times a second to decide whether to draw the key as white or glowing neon cyan.
*   **Event Driven Architecture:**
*   **Collision Detection (collidepoint):** Tracking mouse clicks requires geometry. Pygame's self.rect.collidepoint(mouse_pos) automatically checks if the mathematical coordinates of the user's mouse click fall inside the boundaries of that specific key's rectangle.
*   **The Game/App Loop:** Unlike simple script tutorials that run once and stop, interactive apps use an infinite while loop. It constantly checks for inputs, updates positions, and redraws the screen 60 times every second.
*   **Event Polling:** pygame.event.get() captures everything the user does (mouse movements, clicks, keyboard presses). Right now, it only checks if you clicked the "X" to close the app.
*   **Double Buffering:** pygame.display.flip() acts like a digital canvas flip. Pygame draws everything behind the scenes first, then flips the canvas instantly so the user never sees stuttering or flickering.
*   **Low-Latency Digital Signal Processing (DSP):** I manually pre-initialized Pygame's mixer stream data block structures (44100Hz, 16-bit, 512 buffer) to resolve audio-visual drift lag.
*   **Algorithmic Asset Generation:** I leveraged pure mathematical vector sound synthesis matrices (numpy.linspace and numpy.sin) to dynamically generate real-time 44.1kHz audio sound waves on the fly instead of relying on slow disk-read storage fetches.
*   **Convert to Desktop App:** I used pyinstaller --onefile --noconsole --name="Matcha_Studio" app.py





---


## ⚙️ How to Run These Projects

### 1. Clone the Repository
```bash
git clone https://github.com
cd python-projects
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Each project folder contains its own requirements, or you can install global dependencies here:
```bash
pip install -r requirements.txt
```

---

## 📬 Contact & Connect
*   **LinkedIn:** https://www.linkedin.com/in/jazzmine-elimimian
*   **Email:**
*   **Portfolio Website:** 

