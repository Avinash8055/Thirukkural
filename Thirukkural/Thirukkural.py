import sys
import pandas as pd
import elevenlabs
import speech_recognition as sr
from tkinter import *
from PIL import Image, ImageTk
import os

# Set ElevenLabs API key
elevenlabs.set_api_key("sk_fd4cb4f1dcc96d4c41bea9c7f48ac26c5a911cff5b501b22")
sys.stdout.reconfigure(encoding="utf-8")

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio, language='ta-IN')
        print("You said:", text)
        searching(text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Error occurred; {e}")
        return None

# Function to search for the corresponding Kural and explanation
def searching(text):
    print("Searching for Kural...")

    # Reading Kurals from File
    kural_csv_path = os.path.join("Thirukkural file Path")
    explanation_csv_path = os.path.join("Explanation file Path")
    
    try:
        kural_df = pd.read_csv(kural_csv_path)
        explanation_df = pd.read_csv(explanation_csv_path)
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return
    
    # Slicing Kural from Dataframe
    try:
        kural_verses = kural_df['Verse']
    except Exception as e:
        return

    # Dictionary to store first word of every Kural
    first_dict = {}
    for i in range(len(kural_verses)):
        word = kural_verses.iloc[i].split('\t')[0]
        first_dict[i] = word
    
   
    
    # Searching which word matches with the speech recognized text  
    for i, word in first_dict.items():
        if text == word:
            kural = kural_verses.iloc[i].split('\t\t\t')
            line1 = kural[0].replace('\t', ' ')
            line2 = kural[1].replace('\t', ' ')
            explanation = explanation_df['Explanation'].iloc[i]
            display(line1, line2, explanation)
            text_to_speech(kural_verses.iloc[i], explanation)
            return  # Exit after finding the match
    print("No matching Kural found.")

# Function to convert text to speech
def text_to_speech(TamilText, Explanation):
    try:
        audio_kural = elevenlabs.generate(
            text=TamilText,
            voice="Bill",
            model='eleven_multilingual_v2'
        )
        explanation_text = Explanation
        audio_explanation = elevenlabs.generate(
            text=explanation_text,
            voice="Bill",
            model='eleven_multilingual_v2'
        )
        elevenlabs.play(audio_kural)
        elevenlabs.play(audio_explanation)
    except Exception as e:
        print(f"An error occurred during text-to-speech: {e}")

# Function to display the Kural in the Tkinter window
def display(TamilText, tamil, explanation):
    l1.config(text=TamilText)
    l2.config(text=tamil)
    l3.config(text=explanation)

# Tkinter window setup
root = Tk()
root.title("Thirukkural App")
root.geometry("450x400")

image_path = os.path.join("Image mic Path")
image = Image.open(image_path)
image = image.resize((50, 50))
photo = ImageTk.PhotoImage(image)

image2_path = os.path.join("Thiruvalluvar Image Path")
image2 = Image.open(image2_path)
image2 = image2.resize((150, 200))
photo2 = ImageTk.PhotoImage(image2)

image3_path = os.path.join("Thirukkural BG Path")
image3 = ImageTk.PhotoImage(Image.open(image3_path))

label = Label(root, image=image3)
label.place(x=0, y=0)

welcome = Label(root, text="Speech Recognition")
welcome.place(x=150, y=10)

btn = Button(root, image=photo, command=speech_to_text)
btn.place(x=200, y=240)

Label(root, image=photo2).place(x=10, y=100)

l1 = Label(root, text="")
l1.place(x=180, y=100)
l2 = Label(root, text="")
l2.place(x=180, y=120)
l3 = Label(root, text="", wraplength=400)
l3.place(x=180, y=150)

root.resizable(0, 0)
root.mainloop()
