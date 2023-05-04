import os
import sys
import openai
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QSizePolicy
import datetime
import string
import threading
from google.cloud import texttospeech
import pygame  # Install this library using pip install pygame
from io import BytesIO
import requests
import json
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os.path

def display_image(self, image_url, image_description):
    image_label = QLabel()
    pixmap = QPixmap()
    pixmap.loadFromData(requests.get(image_url).content)
    pixmap = pixmap.scaled(256, 256, Qt.KeepAspectRatio)
    
    # Save image to the 'photos' folder with description as filename
    photos_folder = "photos"
    if not os.path.exists(photos_folder):
        os.makedirs(photos_folder)
    
    image_filename = f"{image_description}.png"
    image_path = os.path.join(photos_folder, image_filename)
    pixmap.save(image_path)

    image_label.setPixmap(pixmap)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("padding: 6px; border-radius: 4px;")

    item = QListWidgetItem()
    item.setSizeHint(label.sizeHint())
    self.chat_list.addItem(item)
    self.chat_list.setItemWidget(item, label)

def generate_image(prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {'YOUR_OPENAI_API_KEY'}",
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        return image_url
    else:
        print(f"Error: {response.status_code}")
        print(response.text)  # Add this line to print the response text
        return None


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keys/YOUR_GOOGLE_CLOUD_JSON_FILE.json'


# Set up the OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

# Implement Speech-to-Text
def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Recognized text:", text)
        return text
    except Exception as e:
        print("Error:", e)
        return None

# Implement Text-to-Voice
def speak(text):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
)

response = client.synthesize_speech(
    input=input_text, voice=voice, audio_config=audio_config
)

with BytesIO(response.audio_content) as audio_file:
    audio_file.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("AI Assistant")

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        vbox = QVBoxLayout(main_widget)

        self.chat_list = QListWidget()
        vbox.addWidget(self.chat_list)

        hbox = QHBoxLayout()

        self.text_edit = QTextEdit()
        hbox.addWidget(self.text_edit)

        self.send_button = QPushButton("Send")
        hbox.addWidget(self.send_button)

        vbox.addLayout(hbox)

        self.send_button.clicked.connect(self.send_text)

        self.show()

    def send_text(self):
        text = self.text_edit.toPlainText()
        self.text_edit.clear()

        if text.strip():
            self.add_message(text, "You")
            threading.Thread(target=self.process_text, args=(text,)).start()

    def add_message(self, text, sender):
        label = QLabel(f"<b>{sender}:</b> {text}")
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)

        item = QListWidgetItem()
        item.setSizeHint(label.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, label)

    def process_text(self, text):
        response = generate_text(text)
        self.add_message(response, "Assistant")
        speak(response)

app = QApplication(sys.argv)
window = App()
sys.exit(app.exec_())

