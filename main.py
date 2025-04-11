import os
import sys
import webbrowser
import datetime
import wikipedia
import pyttsx3
import speech_recognition as sr
import pywhatkit
import threading
import requests
import json
import wolframalpha
import pyjokes
import smtplib
import pyautogui
import screen_brightness_control as sbc
from email.message import EmailMessage
from newsapi import NewsApiClient
import speedtest
import psutil
from bs4 import BeautifulSoup
import platform
import cpuinfo
import GPUtil
from pygame import mixer
import keyboard
import pyperclip
import subprocess
import time

# Configuration
NEWS_API_KEY = 'your_newsapi_key'
WOLFRAM_APP_ID = 'your_wolframalpha_appid'
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'

class UltimateAssistant:
    def __init__(self):
        # Initialize engines
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 180)
        self.recognizer = sr.Recognizer()
        self.listening = True
        self.newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        self.wolfram = wolframalpha.Client(WOLFRAM_APP_ID)
        mixer.init()
        
        # State tracking
        self.current_app = None
        self.email_mode = False
        self.reminders = []

    # Core Functions
    def speak(self, audio):
        print(f"HandiMate: {audio}")
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_command(self, timeout=5):
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=timeout)
                query = self.recognizer.recognize_google(audio).lower()
                print(f"You: {query}")
                return query
            except Exception as e:
                print(f"Error: {e}")
                return None

    # ========== PRODUCTIVITY ========== #
    def create_reminder(self):
        self.speak("What should I remind you about?")
        reminder = self.take_command()
        self.speak("When should I remind you? Say in hours and minutes.")
        when = self.take_command()
        # Parse time and add to reminders list
        self.reminders.append((reminder, when))
        self.speak(f"Reminder set: {reminder} at {when}")

    def check_reminders(self):
        now = datetime.datetime.now().strftime("%H:%M")
        for reminder, time in self.reminders:
            if time in now:
                self.speak(f"Reminder: {reminder}")
                self.reminders.remove((reminder, time))

    def take_screenshot(self):
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        self.speak(f"Screenshot saved as {filename}")

    def type_for_me(self):
        self.speak("What should I type?")
        text = self.take_command(timeout=10)
        pyautogui.write(text, interval=0.1)
        self.speak("Text typed")

    # ========== SYSTEM CONTROL ========== #
    def system_info(self):
        system = platform.system()
        processor = cpuinfo.get_cpu_info()['brand_raw']
        cores = psutil.cpu_count(logical=False)
        ram = round(psutil.virtual_memory().total / (1024**3), 2)
        gpus = GPUtil.getGPUs()
        
        info = f"""
        System: {system}
        Processor: {processor}
        Cores: {cores}
        RAM: {ram} GB
        GPU: {gpus[0].name if gpus else 'None'}
        """
        self.speak(info)

    def battery_status(self):
        battery = psutil.sensors_battery()
        self.speak(f"Battery at {battery.percent}%")
        if battery.power_plugged:
            self.speak("Power source: plugged in")
        else:
            self.speak(f"Estimated time remaining: {battery.secsleft//3600} hours")

    def set_brightness(self, level):
        sbc.set_brightness(level)
        self.speak(f"Brightness set to {level}%")

    # ========== COMMUNICATION ========== #
    def send_email(self):
        self.email_mode = True
        self.speak("Email mode activated. Who should I send to?")
        to = self.take_command()
        
        self.speak("What's the subject?")
        subject = self.take_command()
        
        self.speak("And the message?")
        body = self.take_command()
        
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = to
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            
            self.speak("Email sent successfully")
        except Exception as e:
            self.speak(f"Failed to send email: {e}")
        finally:
            self.email_mode = False

    # ========== KNOWLEDGE ========== #
    def wolfram_query(self, query):
        try:
            res = self.wolfram.query(query)
            answer = next(res.results).text
            self.speak(f"According to Wolfram Alpha: {answer}")
        except:
            self.speak("I couldn't find an answer to that")

    def get_news(self, category='general'):
        try:
            news = self.newsapi.get_top_headlines(category=category, language='en')
            for i, article in enumerate(news['articles'][:5], 1):
                self.speak(f"News {i}: {article['title']}")
        except:
            self.speak("Couldn't fetch news right now")

    # ========== ENTERTAINMENT ========== #
    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.speak(joke)

    def play_radio(self, station="bbc"):
        stations = {
            "bbc": "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_p",
            "classical": "http://stream.classical102.com:8000/classical102",
            "jazz": "http://jazz-wr04.ice.infomaniak.ch/jazz-wr04-128.mp3"
        }
        url = stations.get(station.lower(), stations["bbc"])
        threading.Thread(target=mixer.music.load, args=(url,)).start()
        mixer.music.play()
        self.speak(f"Playing {station} radio")

    # ========== SMART HOME ========== #
    def control_lights(self, action="on"):
        # Integration with Philips Hue/SmartThings would go here
        self.speak(f"Turning lights {action}")

    # ========== MAIN LOOP ========== #
    def process_command(self, query):
        if not query:
            return

        # Check reminders first
        self.check_reminders()

        # Command mapping (50+ commands)
        commands = {
            # Productivity
            'remind me': self.create_reminder,
            'take screenshot': self.take_screenshot,
            'type this': self.type_for_me,
            
            # System
            'system info': self.system_info,
            'battery status': self.battery_status,
            'set brightness to': lambda: self.set_brightness(int(query.split()[-1])),
            
            # Communication
            'send email': self.send_email,
            
            # Knowledge
            'calculate': lambda: self.wolfram_query(query),
            'news': lambda: self.get_news(query.split()[-1] if len(query.split()) > 1 else 'general'),
            
            # Entertainment
            'tell joke': self.tell_joke,
            'play radio': lambda: self.play_radio(query.split()[-1] if len(query.split()) > 2 else 'bbc'),
            
            # Smart Home
            'lights on': lambda: self.control_lights("on"),
            'lights off': lambda: self.control_lights("off"),
            
            # (Include all your original commands here too)
        }

        for cmd, action in commands.items():
            if cmd in query:
                action()
                return

        self.speak("I didn't understand that command")

    def run(self):
        self.speak("Ultimate HandiMate activated. How may I assist?")
        while self.listening:
            query = self.take_command()
            if query:
                if "goodbye" in query:
                    self.speak("Shutting down. Have a great day!")
                    break
                self.process_command(query)

if __name__ == "__main__":
    assistant = UltimateAssistant()
    assistant.run()
