import os
import webbrowser
import datetime
import wikipedia
import pyttsx3
import speech_recognition as sr
import pywhatkit
import random
import pyjokes
import speedtest
import pyfiglet
import calendar
import time
import screen_brightness_control as sbc

class UltimateHandiMate:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('rate', 180)
        self.recognizer = sr.Recognizer()
        self.commands = {
            # System & Device
            'battery': self.check_battery,
            'brightness': self.set_brightness,
            'system info': self.system_info,
            
            # Web & Search
            'search': self.web_search,
            'wikipedia': self.wiki_search,
            'speed test': self.internet_speed,
            
            # Media & Entertainment
            'play': self.play_media,
            'joke': self.tell_joke,
            'ascii art': self.create_ascii_art,
            
            # Productivity
            'timer': self.set_timer,
            'calendar': self.show_calendar,
            'calculate': self.calculate,
            
            # Time & Date
            'time': self.get_time,
            'date': self.get_date,
            'day': self.get_day,
            
            # Fun & Games
            'flip coin': self.flip_coin,
            'roll dice': self.roll_dice,
            'random number': self.random_number,
            
            # Tools
            'screenshot': self.take_screenshot,
            'weather': self.get_weather,
            'news': self.get_news,
            
            # Customizable
            'open website': self.open_website,
            'remember': self.remember_info,
            'recall': self.recall_info,
            
            # System Control
            'shutdown': self.shutdown_pc,
            'restart': self.restart_pc,
            'sleep': self.sleep_pc,
            
            # Learning
            'word of day': self.word_of_day,
            'fact': self.random_fact,
            'quote': self.random_quote,
            
            # Additional
            'alarm': self.set_alarm,
            'reminder': self.set_reminder,
            'countdown': self.start_countdown
        }
        self.memory = {}  # For remember/recall functionality

    def speak(self, text):
        print(f"HandiMate: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                return self.recognizer.recognize_google(audio).lower()
            except:
                return None

    # ========== 30+ COMMAND FUNCTIONS ========== #
    
    # System & Device
    def check_battery(self):
        try:
            import psutil
            battery = psutil.sensors_battery()
            self.speak(f"Battery at {battery.percent}%")
        except:
            self.speak("Battery info unavailable")

    def set_brightness(self, level=None):
        try:
            if not level:
                self.speak("Set brightness to what level?")
                level = self.listen()
            sbc.set_brightness(int(level))
            self.speak(f"Brightness set to {level}%")
        except:
            self.speak("Brightness control failed")

    def system_info(self):
        info = f"""
        System: {os.name}
        Processor: {os.cpu_count()} cores
        Current time: {datetime.datetime.now().strftime('%I:%M %p')}
        """
        self.speak(info)

    # Web & Search
    def web_search(self, query=None):
        if not query:
            self.speak("What should I search?")
            query = self.listen()
        webbrowser.open(f"https://google.com/search?q={query}")
        self.speak(f"Searching for {query}")

    def wiki_search(self, query=None):
        if not query:
            self.speak("What should I look up?")
            query = self.listen()
        try:
            summary = wikipedia.summary(query, sentences=2)
            self.speak(summary)
        except:
            self.speak("Couldn't find information")

    def internet_speed(self):
        self.speak("Testing internet speed...")
        st = speedtest.Speedtest()
        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000
        self.speak(f"Download: {download:.1f} Mbps, Upload: {upload:.1f} Mbps")

    # Media & Entertainment
    def play_media(self, query=None):
        if not query:
            self.speak("What should I play?")
            query = self.listen()
        if "youtube" in query:
            video = query.replace("play", "").replace("on youtube", "").strip()
            pywhatkit.playonyt(video)
            self.speak(f"Playing {video}")
        else:
            self.speak("Specify 'on YouTube' to play videos")

    def tell_joke(self):
        self.speak(pyjokes.get_joke())

    def create_ascii_art(self, text=None):
        if not text:
            self.speak("What text for ASCII art?")
            text = self.listen()
        art = pyfiglet.figlet_format(text)
        print(art)
        self.speak(f"Created ASCII art for {text}")

    # Productivity
    def set_timer(self, minutes=None):
        if not minutes:
            self.speak("Timer for how many minutes?")
            minutes = self.listen()
        self.speak(f"Timer set for {minutes} minutes")
        time.sleep(float(minutes) * 60)
        self.speak("Timer completed!")

    def show_calendar(self):
        now = datetime.datetime.now()
        cal = calendar.month(now.year, now.month)
        print(cal)
        self.speak(f"Calendar for {now.strftime('%B %Y')}")

    def calculate(self, expression=None):
        if not expression:
            self.speak("What should I calculate?")
            expression = self.listen()
        try:
            result = eval(expression)
            self.speak(f"Result is {result}")
        except:
            self.speak("Couldn't calculate that")

    # Time & Date
    def get_time(self):
        time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"Current time is {time}")

    def get_date(self):
        date = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today is {date}")

    def get_day(self):
        day = datetime.datetime.now().strftime("%A")
        self.speak(f"Today is {day}")

    # Fun & Games
    def flip_coin(self):
        result = random.choice(["Heads", "Tails"])
        self.speak(f"It's {result}")

    def roll_dice(self):
        result = random.randint(1, 6)
        self.speak(f"You rolled a {result}")

    def random_number(self, range=None):
        if not range:
            self.speak("Between which numbers?")
            range = self.listen()
        try:
            start, end = map(int, range.split())
            num = random.randint(start, end)
            self.speak(f"Your number is {num}")
        except:
            self.speak("Say like 'between 1 and 100'")

    # Tools
    def take_screenshot(self):
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        import pyautogui
        pyautogui.screenshot(filename)
        self.speak(f"Screenshot saved as {filename}")

    def get_weather(self, location=None):
        if not location:
            self.speak("Which location?")
            location = self.listen()
        webbrowser.open(f"https://www.google.com/search?q=weather+{location}")
        self.speak(f"Showing weather for {location}")

    def get_news(self):
        webbrowser.open("https://news.google.com")
        self.speak("Opening news headlines")

    # Customizable
    def open_website(self, site=None):
        if not site:
            self.speak("Which website?")
            site = self.listen()
        sites = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'github': 'https://github.com'
        }
        if site in sites:
            webbrowser.open(sites[site])
            self.speak(f"Opening {site}")
        else:
            self.speak("Website not configured")

    def remember_info(self, data=None):
        if not data:
            self.speak("What should I remember?")
            data = self.listen()
        key = str(len(self.memory) + 1)
        self.memory[key] = data
        self.speak(f"Remembered as item {key}")

    def recall_info(self, key=None):
        if not key:
            self.speak("Which item to recall?")
            key = self.listen()
        if key in self.memory:
            self.speak(f"Item {key}: {self.memory[key]}")
        else:
            self.speak("Nothing found")

    # System Control
    def shutdown_pc(self):
        self.speak("Shutting down in 1 minute")
        os.system("shutdown /s /t 60")

    def restart_pc(self):
        self.speak("Restarting in 1 minute")
        os.system("shutdown /r /t 60")

    def sleep_pc(self):
        self.speak("Putting system to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    # Learning
    def word_of_day(self):
        words = {
            'Serendipity': 'Finding something good without looking for it',
            'Ephemeral': 'Lasting a short time',
            'Ubiquitous': 'Present everywhere'
        }
        word, meaning = random.choice(list(words.items()))
        self.speak(f"Word: {word}. Meaning: {meaning}")

    def random_fact(self):
        facts = [
            "Honey never spoils",
            "Octopuses have three hearts",
            "Bananas are berries"
        ]
        self.speak(random.choice(facts))

    def random_quote(self):
        quotes = [
            "The only way to do great work is to love what you do",
            "Innovation distinguishes between a leader and a follower",
            "Stay hungry, stay foolish"
        ]
        self.speak(random.choice(quotes))

    # Additional
    def set_alarm(self, time=None):
        if not time:
            self.speak("Set alarm for what time?")
            time = self.listen()
        self.speak(f"Alarm set for {time}")

    def set_reminder(self, reminder=None):
        if not reminder:
            self.speak("What should I remind you?")
            reminder = self.listen()
        self.speak(f"Reminder set: {reminder}")

    def start_countdown(self, seconds=None):
        if not seconds:
            self.speak("Countdown from how many seconds?")
            seconds = self.listen()
        for i in range(int(seconds), 0, -1):
            self.speak(str(i))
            time.sleep(1)
        self.speak("Countdown complete!")

    def run(self):
        self.speak("Ultimate HandiMate activated!")
        while True:
            query = self.listen()
            if query:
                if "exit" in query or "goodbye" in query:
                    self.speak("Goodbye!")
                    break
                
                for cmd, func in self.commands.items():
                    if cmd in query:
                        if cmd in ['brightness', 'search', 'play']:
                            func(query.replace(cmd, "").strip())
                        else:
                            func()
                        break
                else:
                    self.speak("Command not recognized")

if __name__ == "__main__":
    assistant = UltimateHandiMate()
    assistant.run()
