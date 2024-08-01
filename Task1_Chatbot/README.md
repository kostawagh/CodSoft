# NOVA v1.2

## Description

NOVA is a Python-based digital personal assistant with a GUI made using Tkinter. It is designed to handle various user inputs and provide responses. This project showcases practical implementations of AI and some basic natural language processing features. NOVA includes functionalities such as time-based greetings, typo correction, Wikipedia search, and more.


## Features

- **Greeting the User:**
  - Time-based greetings (Good morning, Good afternoon, Good evening)
  - Greeting in response to common greetings (hi, hello, hola, etc.)

- **Command Handling:**
  - Display current time
  - Provide an introduction about the assistant
  - Suggest corrections for inputs close to valid commands
  - Open websites like YouTube, Gmail, Spotify, and Google Drive to increase productivity
  - Perform a Wikipedia search
  - Mini built-in calculator
  - Exit the chat window


## Command Functions

The `commands.py` file contains the core functionality for handling user commands in NOVA:

- **`greet()`**:                    Provides a random greeting message.
- **`helpMenu()`**:                 Returns a list of available commands.
- **`showTime()`**:                 Displays the current time in a human-readable format.
- **`intro()`**:                    Gives an introduction about NOVA.
- **`suggest_Correction(prompt)`**: Suggests corrections for user input based on a predefined list of commands.
- **`openSite(site)`**:             Opens a specified website in a new browser tab.
- **`moreOnDev()`**:                Opens a link to the developer’s LinkedIn profile.


## Usage

1) Run the **nova.py** file 

2) Interact with the Assistant:
    - Type commands or questions in the input area and press Enter.
    - NOVA will respond based on the rules defined (knowledge base)


## Project Structure

**CodSoft Repo**
- **NOVA.py**: Main application file containing the Tkinter GUI and core logic.
- **commands.py**: Module with command functions used by NOVA.
- **README.md**: This file.


## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Contact
For any questions or feedback, please contact:
- Name: Kaustubh Wagh
- Email: kaustubh.wagh@mitaoe.ac.in
 -GitHub: kostawagh
