import openai
import speech_recognition as sr
from gtts import gTTS
import os
import random

# Set up your OpenAI API key
openai.api_key = 'YOUR-OPENAI-API-KEY'

# Create a recognizer object for speech recognition
recognizer = sr.Recognizer()

# Initialize state variables
listening_for_wake_word = True
wake_word = "activate jeff"  # Change to desired wake word

robot_phrases = [
    "Hello, world",
    "Ask me anything!",
    "What's up!",
    "Hello, there",
    "My name is Jeff!"
]

while True:
    if listening_for_wake_word:
        # Capture audio from the microphone
        with sr.Microphone() as source:
            print("Say something...")
            audio = recognizer.listen(source)

        # Recognize the captured audio for the wake word
        try:
            detected_word = recognizer.recognize_google(audio)
            print("Detected word:", detected_word)

            if wake_word.lower() in detected_word.lower():
                wakespeech = random.choice(robot_phrases)
                tts = gTTS(wakespeech, lang="en-GB")
                tts.save("/PATH/TO/YOUR/DIRECTORY/response.mp3")
                os.system("mpg321 /PATH/TO/YOUR/DIRECTORY/response.mp3")  # You may need to install mpg321

                listening_for_wake_word = False
                print("Wake word detected. You can now ask a question.")
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

    else:
        # Capture user input after the wake word
        with sr.Microphone() as source:
            print("Ask a question...")
            audio = recognizer.listen(source)

        # Recognize the captured user input
        try:
            user_input = recognizer.recognize_google(audio)
            print("You asked:", user_input)

            # Generate a response using GPT-3
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": user_input + " [You can add a customize Jeff's personality here] (all responses should be 20-50 words long max)",
                    }
                ],
                temperature=1,
                max_tokens=50,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            content = response["choices"][0]["message"]["content"]
            print(content)

            # Convert the GPT-3 response to speech using Google text
            tts = gTTS(content, lang="en-GB")
            tts.save("/home/pi/boothrobot/response.mp3")

            # Play the generated speech
            os.system("mpg321 /home/pi/boothrobot/response.mp3")  # You may need to install mpg321

            # After responding, go back to listening for the wake word
            listening_for_wake_word = True
        # Handle faliures
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
