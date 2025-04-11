# 🤖 Ultimate HandiMate – Your Personal AI Assistant (Python)

Ultimate HandiMate is a voice-controlled AI desktop assistant built using Python. It performs a wide variety of tasks including productivity aids, system control, entertainment, communication, and more—all through voice commands.

---

## 🎯 Features

### 🧠 Core Abilities
- Natural voice interaction (speech recognition + text-to-speech)
- Wakeup and command loop with graceful shutdown
- Intelligent command processing

### 📅 Productivity
- Voice-based reminders
- Screenshot capture
- Auto typing via voice

### 🖥️ System Control
- Battery status updates
- Brightness adjustment
- System hardware info (CPU, GPU, RAM)

### 📧 Communication
- Email composition and sending via voice
- Secure login via Gmail SMTP

### 📚 Knowledge and Tools
- Wolfram Alpha queries
- Wikipedia search
- News headlines (via NewsAPI)

### 🎵 Entertainment
- Tell jokes using `pyjokes`
- Stream live radio (BBC, Jazz, Classical)

### 💡 Smart Home (Prototype)
- Simulated control of smart home lights

---

## 🛠️ Tech Stack & Libraries

- `pyttsx3` – Text-to-speech engine
- `speech_recognition` – Speech-to-text
- `pywhatkit` – YouTube and WhatsApp automation
- `pyautogui` – GUI automation
- `wolframalpha` – Computational intelligence
- `newsapi` – News headlines
- `psutil`, `cpuinfo`, `GPUtil` – System monitoring
- `pyjokes` – Random jokes
- `pygame.mixer` – Audio playback
- `keyboard`, `pyperclip`, `subprocess`, `webbrowser` – Utility modules

---

## 🔧 Setup Instructions

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt

2. Replace API Keys and Credentials: Open the Python file and replace the placeholders with your credentials:

-NEWS_API_KEY = 'your_newsapi_key'
-WOLFRAM_APP_ID = 'your_wolframalpha_appid'
-EMAIL_ADDRESS = 'your_email@gmail.com'
-EMAIL_PASSWORD = 'your_app_password'

3. Run the assistant:
   ```bash
   python main.py
🔒 Security Note
For email to work, you must use an App Password (not your main password). Do not share your credentials in public repositories.

📌 To-Do & Ideas
-GUI interface

-Wake word detection

-Face recognition integration

-Smart home real device control (Philips Hue, etc.)

-Weather & location-based actions

📜 License
This project is licensed under the Non-Commercial License.
For commercial use inquiries, please contact [nadimmostofa2012@gmail.com].

🤝 Contributing
-Pull requests are welcome! For major changes, please open an issue first.

📧 Contact
-Nadim Mostofa - @Nadim-saas
-Project Link: https://github.com/Nadim-saas/HandiMate
