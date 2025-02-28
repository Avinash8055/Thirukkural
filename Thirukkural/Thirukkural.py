import sys
from dotenv import load_dotenv
import pandas as pd
import elevenlabs
from elevenlabs.client import ElevenLabs 
import speech_recognition as sr
from tkinter import *
from PIL import Image, ImageTk
import os
from elevenlabs import text_to_speech, play

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

# Initialize ElevenLabs client
if not api_key:
    raise ValueError("API Key not found! Check your .env file.")

client = ElevenLabs(api_key=api_key)
#elevenlabs.set_api_key("")
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
    kural_csv_path = os.path.join("Thirukkural File Path")
    explanation_csv_path = os.path.join("Explanation File Path")
    
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
            # Display first, then do text-to-speech
            display(line1, line2, explanation)
            text_to_speech(kural_verses.iloc[i], explanation)
            return
    print("No matching Kural found.")


def text_to_speech(TamilText, Explanation):
    try:
        # Generate audio for Tamil text
        audio_kural = client.text_to_speech.convert(
            text=TamilText,
            voice_id="",
            model_id="eleven_multilingual_v2"
        )

        # Generate audio for explanation
        audio_explanation = client.text_to_speech.convert(
            text=Explanation,
            voice_id="",
            model_id="eleven_multilingual_v2"
        )

        # Play the generated audio
        play(audio_kural)
        play(audio_explanation)

    except Exception as e:
        print(f"An error occurred during text-to-speech: {e}")

# Define a color that matches your background
BG_COLOR = "#f5f5f5"  # Light gray - adjust this hex color to match your background

# Function to display the Kural in the Tkinter window
def display(TamilText, tamil, explanation):
    l1.config(text=TamilText, 
              font=("Arial", 12, "bold"),
              fg="black",
              bg=BG_COLOR,
              wraplength=350)
    
    l2.config(text=tamil, 
              font=("Arial", 12, "bold"),
              fg="black", 
              bg=BG_COLOR,
              wraplength=350)
    
    l3.config(text=explanation, 
              font=("Arial", 11),
              fg="black",
              bg=BG_COLOR,
              wraplength=350,
              justify="left")
    
    root.update()

# Tkinter window setup
root = Tk()
root.title("Thirukkural App")
root.geometry("600x700")

# Load and resize images
image_path = os.path.join("mic img path")
image = Image.open(image_path)
image = image.resize((50, 50))
photo = ImageTk.PhotoImage(image)

image2_path = os.path.join("Thiruvalluvar img path")
image2 = Image.open(image2_path)
image2 = image2.resize((150, 200))
photo2 = ImageTk.PhotoImage(image2)

# Load and resize background image to match window size
image3_path = os.path.join("ThirukuralBackground img path")
background_image = Image.open(image3_path)
background_image = background_image.resize((600, 700))  # Match window size
image3 = ImageTk.PhotoImage(background_image)

# Create background label
background_label = Label(root, image=image3)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Update other labels
welcome = Label(root, 
               text="Thirukkural Speech Recognition",
               font=("Arial", 16, "bold"),
               bg=BG_COLOR)
welcome.place(x=150, y=20)

btn = Button(root, image=photo, command=speech_to_text)
btn.place(x=275, y=600)

Label(root, image=photo2).place(x=20, y=100)

# Place labels
l1 = Label(root, text="", padx=10, pady=5, bg=BG_COLOR)
l1.place(x=200, y=150)

l2 = Label(root, text="", padx=10, pady=5, bg=BG_COLOR)
l2.place(x=200, y=200)

l3 = Label(root, text="", padx=10, pady=5, bg=BG_COLOR)
l3.place(x=200, y=250)

root.resizable(0, 0)
root.mainloop()