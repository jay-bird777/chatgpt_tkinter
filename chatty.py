import openai
import speech_recognition as sr
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk
from PIL import Image, ImageTk

import customtkinter

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M")


# Set up OpenAI API credentials
openai.api_key = ''

def ask_openai(question):
    model_engine = "text-davinci-003"
    prompt = f"Q: {question}\nA:"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = completions.choices[0].text.strip()
    return message

# Function to recognize speech using microphone
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand you."
    except sr.RequestError:
        return "Sorry, my speech recognition service is currently down."

#class ChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Baymax")
        self.window.geometry("400x600")
    

        self.scroll_frame = tk.Frame(self.window)
        self.scroll_frame.pack(side="top", fill="both", expand=True)

        self.chat_history = tk.Text(self.scroll_frame, wrap="word", state="disabled")
        self.chat_history.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.scroll_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_history.configure(yscrollcommand=self.scrollbar.set, bg= 'white')

        self.question_entry = tk.Entry(self.window, width=200, font=("Arial", 12))
        self.question_entry.pack(pady=10)

        self.ask_button = tk.Button(self.window, text="Ask", width=200, command=self.ask_question, font=("Arial", 12))
        self.ask_button.pack(pady=10)

        self.clear_button = tk.Button(self.window, text="Clear", width=200, command=self.clear_all, font=("Arial", 12))
        self.clear_button.pack(pady=10)

        self.listen_button = tk.Button(self.window, text="Speak",width=200, command=self.listen_question, font=("Arial", 12))
        self.listen_button.pack(pady=10)

        self.window.mainloop()


    def clear_all(self):
        self.chat_history.configure(state="normal")
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.configure(state="disabled")

    def ask_question(self):
        question = self.question_entry.get().strip()
        if question != "":
            response = ask_openai(question)
            self.update_chat_history(question, response)

    def listen_question(self):
        question = recognize_speech()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, question)
        response = ask_openai(question)
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state="normal")
        if self.chat_history.index('end') != None:
            self.chat_history.insert('end', "You: " + question + "\n", 'bold')
            self.chat_history.insert('end', "Baymax: " + response + "\n\n")
            self.chat_history.tag_configure('bold', font=("Arial", 12, 'bold'))
            self.chat_history.configure(state="disabled")
            self.chat_history.yview('end')

class ChatGUI:
    def __init__(self):
        #root = customtkinter.CTk()
        self.window = customtkinter.CTk()
        self.window.title("Baymax")
        self.window.geometry("800x800")
        customtkinter.set_appearance_mode("dark")
        self.window.eval("tk::PlaceWindow . center")
    

        self.scroll_frame = customtkinter.CTkFrame(self.window)
        self.scroll_frame.pack(side="top", fill="both", expand=True)
        
        

        self.chat_history = customtkinter.CTkTextbox(self.scroll_frame, wrap="word", state="disabled")
        self.chat_history.pack(side="left", fill="both", expand=True)

        self.scrollbar = customtkinter.CTkScrollbar(self.scroll_frame, orientation="vertical", command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_history.configure(yscrollcommand=self.scrollbar.set)

        self.question_entry = customtkinter.CTkEntry(self.window, width=500, font=("Arial", 12))
        self.question_entry.pack(pady=10)

        self.ask_button = customtkinter.CTkButton(self.window, text="Ask", width=500, command= self.ask_question, font=("Arial", 12))
        self.ask_button.pack(pady=10)

        self.clear_button = customtkinter.CTkButton(self.window, text="Clear", width=500, command=self.clear_all, font=("Arial", 12))
        self.clear_button.pack(pady=10)

        self.listen_button = customtkinter.CTkButton(self.window, text="Speak",width=500, command=self.listen_question, font=("Arial", 12))
        self.listen_button.pack(pady=10)
        
        placeholder_text = 'type here...'
        self.question_entry.insert(0, placeholder_text)
        self.question_entry.bind("<Button-1>", lambda event: clear_entry(event, self.question_entry))
        
        def clear_entry(event, entry):
            entry.delete(0, 'end')
            #entry.unbind('<Button-1>', event)

        self.window.mainloop()


    def clear_all(self):
        self.chat_history.configure(state="normal")
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.configure(state="disabled")

    def ask_question(self):
        question = self.question_entry.get().strip()
        if question != "":
            response = ask_openai(question)
            self.update_chat_history(question, response)

    def listen_question(self):
        question = recognize_speech()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, question)
        response = ask_openai(question)
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state="normal")
        # photo = ImageTk.PhotoImage(Image.open("/Users/demetriousbrown/TK_Chatbot/images.png").resize((30,30)))
        
        # self.ask_button = tk.Button(self.window, width=30,height=30,
        # command=self.ask_question, font=("Arial", 12), image = photo, compound="left"
        # )
        if self.chat_history.index('end') != None:
            self.chat_history.insert('end', "You: " + question + "\n", 'bold')
            self.chat_history.insert('end', "Baymax: " + response + "\n\n")
            #self.chat_history.tag_configure('bold', font=("Arial", 12, 'bold'))
            self.chat_history.configure(state="disabled")
            self.chat_history.yview('end')
            
            # self.chat_history.insert('end', current_time + ' ', ("small", "right", "white"))
            # self.chat_history.window_create('end', window=customtkinter.CTkLabel(self.chat_history, fg="white", text=question,
            # wraplength=200, font=("Arial", 18), bg="#218aff", bd=4, justify="left"))
            # self.chat_history.insert('end','\n\n ', "left")
            # self.chat_history.insert('end',current_time+' ', ("small", "left", "white"))
            # self.chat_history.window_create('end', window=customtkinter.CTkLabel(self.chat_history, fg="white",
            # text=response,
            # wraplength=200, font=("Arial", 18), bg="#aeb9cc", bd=4, justify="right"))
            # self.chat_history.insert('end','\n\n ', "right")
            # self.chat_history.tag_configure("right", justify="right")
            # self.chat_history.tag_configure(foreground="#0000CC", font=("Arial", 12, 'bold'))
            # self.chat_history.configure(state="disabled")
            # self.chat_history.yview('end')

            

if __name__ == "__main__":
    gui = ChatGUI()