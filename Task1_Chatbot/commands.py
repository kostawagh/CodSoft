'''
NOVA v1.2
Command File

--Dev's Note--

This file contains majority of the commands used by NOVAv2 for responding to user inputs
Current functionality:
    
    1) greeting the user at start according to time of the day/night
    2) greeting in response to hi/hello/hola etc
    3) show a help menu
    4) showing current time                                             [using datetime library]
    5) providing an intro
    6) suggest corrections if input is close to a valid command         [using textblob- NLP library]
    7) open websites like Youtube/Spotify/Gmail/Drive                   [using webbrowser library]

Note:
All command functions generally return a string, so that GUI can display text to user
    '''


# Importing all libraries
import datetime
import random
import webbrowser
from textblob import TextBlob
import warnings

# ignoret the wiki warnings
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')



# function to greet 
def greet():
    initial_greetings = [
        "Hello there, How can I assist you today?", 
        "Hi, How can I help you?",
        "Good to see you! How can I be of service?",
        "Hello Again! How may I assist you?"
    ]
    return random.choice(initial_greetings)


# function to show Help Menu
def helpMenu():
    return """Here are the commands you can use:
    
- time:         to get the current time
- help:         to see a list of commands
- intro:        to ask for NOVA's introduction
- wiki:         to search a topic on Wikipedia
- youtube*:     to open YouTube
- music*:       to spotify web player
- gmail*:       to open Gmail
- drive*:       to open google drive
- calc:         to open the calculator
- dev*:         to visit Developer's LinkedIn page
- bye:          to exit NOVA chatbot


(* - NOVA will use your default browser and redirect you to the respective website)

Hope that was helpful. =)"""


# function to show time
def showTime():
    now = datetime.datetime.now()
    
    hour = int(now.strftime("%H"))
    minutes = now.strftime("%M")
    if hour<12:
        hour = str(hour)

        current_time = hour+":"+minutes+" am"
    else:
        hour = hour - 12
        hour = str(hour)
        current_time = hour+":"+minutes+" pm"
    time_responses = [
        f"The current time is {current_time}",
        f"It's {current_time} right now.",
        f"The time now is {current_time}"
    ]
    return random.choice(time_responses)


# function to give NOVA's intro
def intro():
    intro_responses = [
        "Hello, I am NOVA, a Digital Assistant designed by Kaustubh Wagh. I am a rule-based chatbot and I can perform several tasks for you. Use 'help' to know more. Nice to meet you!",
        "Hi there! I’m NOVA, your Digital Assistant, created by Kaustubh Wagh. I’m a rule-based chatobot and I'm always here to assist with various tasks. Use 'help' to find out more. Pleased to meet you!",
        "Hey! I’m NOVA, a Digital Assistant developed by Kaustubh Wagh. I'm a rule-based chatbot and I can help you with many tasks. Type 'help' for more info. Nice to meet you!",
        "Glad you asked! Hello there! I'm NOVA, a digital personal assistant made by Kaustubh Wagh. I work on a rule-based system. Use 'help' command if you want to know more. Please to meet you User"
    ]
    return random.choice(intro_responses)

# function to suggest correction using textblob
def suggest_Correction(prompt):
    blobObj = TextBlob(prompt)
    # all valid commands
    commands = ['time', 'help', 'intro', 'wiki', 'youtube', 'gmail', 'calc', 'bye', 'music', 'drive', 'dev', 'introduce','hello']
    corrected_prompt = str(blobObj.correct())
    
    for command in commands:
        if corrected_prompt in command:
            return command
    return None

# function to open website
def openSite(site):
    try:
        webbrowser.open_new_tab("https://www." + site + ".com")
        return f"Opening {site.capitalize()}..."
    except Exception as e:
        return f"Could not open the site. Details: {e}"
    

def moreOnDev():
    try:
        webbrowser.open_new_tab("https://www.linkedin.com/in/kaustubh-wagh-24288a256")
    except Exception as e:
        return f"Could not open the site. Detail: {e}"
    


'''
Dev's Note

- Study more libraries
- Add more features
- Dont't Give up, Never Ever

-Kosta'''
