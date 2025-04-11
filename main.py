import os
import sys
import webbrowser
import datetime
import wikipedia
import pyttsx3
import speech_recognition as sr
import pywhatkit
import threading

class VoiceAssistant:
    def __init__(self):
        # Initialize voice engine
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 180)
        self.recognizer = sr.Recognizer()
        self.listening = True
        self.current_action = None

    def speak(self, audio):
        """Convert text to speech"""
        print(f"HANDI: {audio}")
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_command(self):
        """Take microphone input and return as text"""
        with sr.Microphone() as source:
            try:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                
                print("Recognizing...")
                query = self.recognizer.recognize_google(audio, language='en-US')
                print(f"You said: {query}")
                return query.lower()
                
            except sr.WaitTimeoutError:
                print("Listening timeout")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                self.speak("I didn't catch that. Please try again.")
                return None
            except sr.RequestError as e:
                print(f"Recognition error: {e}")
                self.speak("There was an error with the speech service.")
                return None

    def play_music(self):
        """Play music from default directory"""
        music_dir = os.path.join(os.path.expanduser('~'), 'Music')
        if os.path.exists(music_dir):
            songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                self.speak("Playing your favorite tunes")
            else:
                self.speak("No music files found")
        else:
            self.speak("Music directory not found")

    def search_google(self):
        """Handle Google search without blocking"""
        self.speak("What would you like me to search on Google?")
        query = self.take_command()
        if query:
            self.speak(f"Searching Google for {query}")
            # Run in background to prevent blocking
            threading.Thread(target=pywhatkit.search, args=(query,)).start()

    def search_youtube(self):
        """Handle YouTube search without blocking"""
        self.speak("What would you like to watch on YouTube?")
        query = self.take_command()
        if query:
            self.speak(f"Playing {query} on YouTube")
            # Run in background to prevent blocking
            threading.Thread(target=pywhatkit.playonyt, args=(query,)).start()

    def search_wikipedia(self, query):
        """Search Wikipedia"""
        query = query.replace("who is", "").replace("who was", "").replace("what is", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            self.speak(f"Here's what I found: {summary}")
        except wikipedia.exceptions.DisambiguationError:
            self.speak("There are multiple matches. Could you be more specific?")
        except wikipedia.exceptions.PageError:
            self.speak("I couldn't find information on that topic.")
        except Exception as e:
            print(f"Wikipedia error: {e}")
            self.speak("There was an error fetching information.")

    def open_program(self, path, name):
        """Open a program"""
        try:
            os.startfile(path)
            self.speak(f"Opening {name} for you")
        except Exception as e:
            print(f"Error opening program: {e}")
            self.speak(f"Sorry, I couldn't open {name}")

    def close_program(self, process_name, name):
        """Close a program"""
        try:
            os.system(f"taskkill /IM {process_name} /F")
            self.speak(f"Closing {name}")
        except Exception as e:
            print(f"Error closing program: {e}")
            self.speak(f"Couldn't close {name}")

    def process_command(self, query):
        """Process and execute user commands"""
        if not query:
            return

        # Website commands
        website_commands = {
            'open youtube': 'https://youtube.com',
            'open google': 'https://google.com',
            'open kaggle': 'https://www.kaggle.com',
            'open chat': 'https://chat.openai.com',
            'open wikipedia': 'https://wikipedia.org',
            'open facebook': 'https://facebook.com',
            'open twitter': 'https://twitter.com',
            'open instagram': 'https://instagram.com',
            'open github': 'https://github.com',
            'open stackoverflow': 'https://stackoverflow.com',
        }

        for cmd, url in website_commands.items():
            if cmd in query:
                self.speak(f"Opening {cmd.replace('open ', '')} for you")
                webbrowser.open(url)
                return

        # Special commands
        if 'play music' in query:
            self.play_music()
        elif 'the time' in query or 'what time is it' in query:
            str_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {str_time}")
        elif 'open code' in query:
            self.open_program("C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", "VS Code")
        elif 'close code' in query:
            self.close_program("Code.exe", "VS Code")
        elif 'open notepad' in query:
            self.open_program("C:\\Windows\\System32\\notepad.exe", "Notepad")
        elif 'close notepad' in query:
            self.close_program("notepad.exe", "Notepad")
        elif 'open calculator' in query:
            self.open_program("C:\\Windows\\System32\\calc.exe", "Calculator")
        elif 'close calculator' in query:
            self.close_program("Calculator.exe", "Calculator")
        elif 'open paint' in query:
            self.open_program("C:\\Windows\\System32\\mspaint.exe", "Paint")
        elif 'close paint' in query:
            self.close_program("mspaint.exe", "Paint")
        elif 'search on google' in query:
            self.search_google()
        elif 'search on youtube' in query:
            self.search_youtube()
        elif 'who is' in query or 'what is' in query:
            self.search_wikipedia(query)
        elif 'quit' in query or 'exit' in query or 'goodbye' in query:
            self.speak("Goodbye! Have a great day!")
            self.listening = False
        else:
            self.speak("I'm not sure how to help with that. Try asking me something else.")

    def startup(self):
        """Initialization sequence"""
        startup_messages = [
            "Initializing HANDI systems",
            "Loading all modules",
            "Checking system resources",
            "Establishing connections",
            "Almost ready",
            "All systems operational",
            "Now at your service"
        ]

        for message in startup_messages:
            self.speak(message)

        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        self.speak(f"{greeting}! I am HANDI, your personal assistant. How can I help you today?")

    def run(self):
        """Main execution loop"""
        self.startup()
        while self.listening:
            query = self.take_command()
            if query:
                self.process_command(query)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
