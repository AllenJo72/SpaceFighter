
import tkinter as tk
from tkinter import ttk
import openai
import pyttsx3
import threading
from gtts import gTTS
import os
import pygame
import librosa
import uuid
import soundfile as sf

openai.api_key = "sk-proj_-IX3_8RyDnh6dFtLupSJMRYfEt1RBKfZOmqzayootNxgMA-XBG1okzE1XtWP6igB6frs3JiKC_92UboOr9vV8oAFC--uoUUiO6PHHw2JLtccCBr80kBIC32RTT3BlbkFJBdGbdJizbXoMy1n2Z1iX6neXyTl"

engine = pyttsx3.init()
pygame.mixer.init()

def get_response(character, user_message):
    if character == "Shakespeare":
        system_message = "You are Shakespeare. Talk to me like Shakespeare only."
    elif character == "Einstein":
        system_message = "You are Albert Einstein. Talk to me like Einstein only."
    elif character == "Hemingway":
        system_message = "You are Ernest Hemingway. Talk to me like Hemingway only."
    else:
        system_message = "You are a wise character. Talk like a philosopher."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, something went wrong."

def send_message():
    user_message = entry.get()  
    character = char_select.get() 

    if user_message.strip():  
        chat_box.config(state=tk.NORMAL)  
        chat_box.insert(tk.END, create_message_box("User", user_message))  
        chat_box.insert(tk.END, "-"*40 + "\n")  
        threading.Thread(target=process_message, args=(character, user_message)).start()
        entry.delete(0, tk.END)  
        chat_box.config(state=tk.DISABLED)

def process_message(character, user_message):
    bot_response = get_response(character, user_message)
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, create_message_box(character, bot_response))
    chat_box.insert(tk.END, "-"*40 + "\n") 
    chat_box.yview(tk.END)  
    chat_box.config(state=tk.DISABLED) 
    speak_text(bot_response)

def speak_text(text):
    # Generate the initial speech audio using gTTS
    tts = gTTS(text, lang='en', slow=False, tld="com.au")
    
    # Generate a unique filename using uuid
    unique_filename = f"response_{uuid.uuid4().hex}.mp3"
    tts.save(unique_filename)

    # Load the audio file using librosa
    y, sr = librosa.load(unique_filename, sr=None)

    # Apply pitch shift (negative for deepening)
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=-3)  # Shift the pitch

    # Generate a unique filename for the deepened audio
    deepened_filename = f"deepened_response_{uuid.uuid4().hex}.wav"
    
    # Save the deepened audio back to a file
    sf.write(deepened_filename, y_shifted, sr)

    # Play the deepened audio using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(deepened_filename)
    pygame.mixer.music.play()

# Helper function to create the message boxes with rounded corners
def create_message_box(sender, text):
    # Create the message box as a formatted string with indentation for styling
    if sender == "User":
        box = f"\n{sender}: {text}\n"
    else:
        box = f"\n{sender}: {text}\n"
    
    return box

# Root window
root = tk.Tk()
root.title("Chat with Great Literature Figures")
root.geometry("600x700")  # Adjusted size
root.config(bg="#2e3b4e")  

# Apply theme
style = ttk.Style(root)
style.theme_use("clam")  # You can try "alt", "azure", or other themes

# Main frame
frame = ttk.Frame(root, padding=10)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Character selection label
char_select_label = ttk.Label(frame, text="Select Character:", font=("Helvetica", 14, "bold"), anchor="w")
char_select_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Character selection dropdown
char_select = ttk.Combobox(frame, values=["Shakespeare", "Einstein", "Hemingway"], state="readonly", font=("Helvetica", 12), width=18)
char_select.set("Shakespeare")  # Default selection
char_select.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Chat box
chat_box = tk.Text(frame, height=15, width=50, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 12), bg="#333333", fg="white", padx=10, pady=10)
chat_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Scrollbar
scrollbar = ttk.Scrollbar(frame, command=chat_box.yview)
scrollbar.grid(row=1, column=2, sticky="ns")
chat_box.config(yscrollcommand=scrollbar.set)

# User message entry field
entry = ttk.Entry(frame, width=40, font=("Helvetica", 12), background="#f1f1f1", foreground="black")
entry.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Send button
send_button = ttk.Button(frame, text="Send", command=send_message, style="TButton", width=15)
send_button.grid(row=2, column=1, padx=10, pady=10)

# Configure grid row and column weight
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Run the application
root.mainloop()
