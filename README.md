# AI-Text-based-Assistant


This repository contains the code for a simple AI text-based assistant using OpenAI's GPT-4 and Google Text-to-Speech. The application allows users to interact with the assistant through a GUI, with the assistant providing responses through text and speech.

Features
Text-based chat interface for interacting with the AI assistant
AI assistant generates responses using OpenAI's GPT-4 model
Text-to-speech functionality using Google Text-to-Speech API
Customizable language and gender for text-to-speech voice
Requirements
To run the application, make sure you have the following installed:

Python 3.6 or later
openai package: pip install openai
google-cloud-texttospeech package: pip install google-cloud-texttospeech
PyQt5 package: pip install PyQt5
pygame package: pip install pygame
Setup
Before running the application, you need to obtain API keys for OpenAI and Google Cloud Text-to-Speech, and set up the appropriate environment variables:

Sign up for an API key from OpenAI and Google Cloud Text-to-Speech.
Replace 'YOUR_OPENAI_API_KEY' and 'YOUR_GOOGLE_CLOUD_JSON_FILE.json' in the code with your actual API keys and the JSON file name.
Personalization
To personalize the text-to-speech voice, you can modify the language_code and ssml_gender parameters in the texttospeech.VoiceSelectionParams function call.

For example, to use a male voice in British English, modify the voice variable as follows:

python
Copy code
voice = texttospeech.VoiceSelectionParams(
    language_code='en-GB',
    ssml_gender=texttospeech.SsmlVoiceGender.MALE,
)
For a full list of supported languages and genders, refer to the Google Cloud Text-to-Speech documentation.

Usage
Run the application using the following command:

bash
Copy code
python ai_assistant.py
A GUI will open, allowing you to interact with the AI assistant by typing messages and receiving both text and audio responses.
