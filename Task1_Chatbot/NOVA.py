'''
NOVA v1.2
Main File

--Dev's Notes--

This file contains the tkinter GUI and the interface to handle the user inputs
Current functionality:

    FROM COMMANDS MODULE
    1) greeting the user at start according to time of the day/night
    2) greeting in response to hi/hello/hola etc
    3) show a help menu
    4) showing current time                                             [using datetime library]
    5) providing an intro
    6) suggest corrections if input is close to a valid command         [using textblob- NLP library]
    7) open websites like Youtube/Spotify/Gmail                         [using webbrowser library]

    FROM THIS FILE
    1) Time-Based greetings (good morning/ good afternoon etc
    2) Wikipedia search             [using wikipedia library]
    3) Mini built-in calculator     [using sympify function of sympy lib]
    4) exiting the chat window      [just exit =)]

Note:
Some function used are from commands module that is in same directory. 
Do not move that file (may crash NOVA)
    '''



# Importing the libraries
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import random
import wikipedia
import sympy
import commands as cmd
import datetime

# NOVA GUI Class holding all functions
class NOVA_GUI(tk.Tk):

    # All functions 
    # Function to create greeting according to time 
    def get_greeting(self):
        now = datetime.datetime.now()
        hour = now.hour
        if 0 <= hour < 12:
            return "Good morning User!"
        elif 12 <= hour < 16:
            return "Good afternoon User!"
        else:
            return "Good evening User!"

    # Dispaly greeting message when NOVA starts
    def time_greeting(self): 
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"NOVA: {self.get_greeting()}\n\n", ('nova',))
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)
        self.greeted = True             # flag for greeting




    # Function to initiate the main chat window
    def __init__(self):
        super().__init__()

        # main window
        self.title("NOVA: Your Digital Assistant")
        self.geometry("400x500")
        self.configure(bg="#1E1E1E")        # Dark background color
        self.font = ('Segoe UI', 10)
        self.greeted = False                # flag to check if greeting is sent

        # Text Display widget
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=self.font, bg="#2e2e2b", fg="#FFFFFF", state=tk.DISABLED)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Tag for white and yellow colors
        self.text_area.tag_configure('user', foreground='#FFFFFF')          # white = user
        self.text_area.tag_configure('nova', foreground='#FFFFAA')          # yellow = nova

        # User Input Area
        self.input_area = tk.Entry(self, font=self.font, bg="#F9F9F9", fg="#333333")
        self.input_area.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)

        # Send button
        self.send_button = tk.Button(self, text="Send", font=self.font, bg="#0033A0", fg="#FFFFFF", command=self.messages)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Key Bindings
        self.bind('<Return>', self.messages)
        self.bind('<Shift-Return>', lambda e: None)  # Prevent event from processing Shift+Enter

        # Display the initial greeting
        self.after(100, self.time_greeting)

    

    # Function to send and receive messages
    def messages(self, event=None):
        user_input = self.input_area.get().strip()
        if user_input:
            self.text_area.config(state=tk.NORMAL)              # allow input in display area       
            
            # input user message
            self.text_area.insert(tk.END, f"You: {user_input}\n", ('user',))
            self.text_area.yview(tk.END)
            self.input_area.delete(0, tk.END)                   

            # input NOVA's response
            response = self.processInput(user_input)
            self.text_area.insert(tk.END, f"NOVA: {response}\n\n", ('nova',))
            self.text_area.yview(tk.END)
            self.text_area.config(state=tk.DISABLED)            # disable input in display area

    # Function to get input and respond accordingly (string matching)
    def processInput(self, user_input):
        user_input = user_input.lower()
        response = ""
        
        if 'time' in user_input:
            response = cmd.showTime()
        elif any(greeting == user_input for greeting in ['hello', 'hi', 'hola', 'hey', 'hii', 'hello there', 'hello again', 'hey there', 'hi there', 'hey you', 'yo',f"what's up",'all good?',"bonjour","hello nova","nova", 'whats up', 'what up']) or any(greeting in user_input for greeting in ['good morning', 'good afternoon', 'good evening']):
            response = cmd.greet()
        elif any(introQuery in user_input for introQuery in ['intro', 'who are you','introduce', 'about you'] ):
            response = cmd.intro()
        elif 'wiki' in user_input:
            response = self.WikiSearch()
        elif 'youtube' in user_input:
            cmd.openSite('youtube')
            response = "Opening YouTube...\nHere we go!"
        elif 'gmail' in user_input:
            cmd.openSite('gmail')
            response = "Opening Gmail...\nGotta check the inbox"
        elif 'music' in user_input:
            cmd.openSite('spotify')
            response = "Opening Spotify Web...\nLet's drop the needle!"
        elif 'calc' in user_input:
            response = self.calculator()
        elif 'drive' == user_input:
            cmd.openSite('drive.google')
            response = "Opening Google Drive...\n"
        elif 'dev' == user_input:
            cmd.moreOnDev()
            response = "Redirecting to my Developer's Page\n"
        elif 'help' in user_input:
            response = cmd.helpMenu()
        elif 'bye' in user_input:
            response = self.exitChat()
        else:
            correction = cmd.suggest_Correction(user_input)
            if correction:
                response = f"Did you mean '{correction}'?"
            else:
                response = random.choice([
                    "Apologies, I did not understand. Try 'help'.",
                    "I'm not sure what you mean. You can type 'help' to see available commands.",
                    "Sorry, I didn't catch that. Maybe 'help' can guide you?"
                ])
        return response
    



    # Function to perfrom a Wikipedia Search
    def WikiSearch(self):
        query = simpledialog.askstring("Wikipedia Search", "What would you like to search about?")
        if query:
            try:
                summary = wikipedia.summary(query, sentences=3)         # will give 3 line summary
                return f"According to Wikipedia...\n{summary}"
            # handle the ambiguous exception
            except wikipedia.exceptions.DisambiguationError as e:
                options = e.options             # closest articles (given by wiki)

                #more than one options
                if len(options) >1:   
                    options = options[:10]                  # limiting list to 10
                    # dialog box to select article
                    
                    optionList = "\n".join([f"{i+1}) {option}" for i,option in enumerate(options)])     # numbered list of options
                    optionChoice = simpledialog.askinteger("Choose Option",f"Your search term is ambiguous. Please choose an option:\n{optionList}\n\Enter the option number you want to search for")

                    # check if choice is valid
                    if optionChoice is not None and optionChoice>=1 and optionChoice<=len(options):
                        selectedOption = options[optionChoice-1]
                        summary = wikipedia.summary(selectedOption,sentences=3)

                        return f"According to Wikipedia...\n{summary}"
                    else:
                        return "Invalid option. Wiki closed"
                
                else:
                # only one option
                    selecedOption = options[0]
                    summary = wikipedia.summary(selectedOption, senetences=3)
                    return f"According to Wikipedia...\n{summary}"
                
            # Page Not found
            except wikipedia.exceptions.PageError:
                return "Sorry, the page was not found."
            # other errors
            except Exception as e:
                return f"Sorry, I couldn't get the information. Error: {e}"
        return "No query entered."

    
    # Mini Calculator function
    def calculator(self):
        equation = simpledialog.askstring("NOVA Calculator", "Enter the Equation")
        if equation:
            try:
                result = sympy.sympify(equation)
                floatResult = float(result.evalf())
                return f"The result is {floatResult:.3f}"  # limiting answer to 3 decimal places
            except Exception:
                return "Error- Invalid Arithmetic Expression"
            

    # function to exit chat
    def exitChat(self):
        self.text_area.config(state=tk.NORMAL)          # allow input in display
        self.text_area.insert(tk.END, "NOVA: Goodbye! Hava a great day!\n\n",('nova',))
        self.text_area.config(state=tk.DISABLED)        # disable input in display
        self.text_area.yview(tk.END)
        self.after(2000, self.quit)                     # wait for 2s and close chat

if __name__ == '__main__':
    app = NOVA_GUI()
    app.mainloop()