# -*- coding: utf-8 -*-
import re
import random
import time
from datetime import datetime

user_name = ""

# ---------------- KNOWLEDGE BASE ---------------- #
knowledge_base = {
    "ai": "AI stands for Artificial Intelligence. It makes machines smart.",
    "python": "Python is a powerful and easy programming language.",
    "chatbot": "A chatbot is a program that talks like a human.",
    "machine learning": "Machine Learning is a subset of AI that learns from data."
}

# ---------------- RESPONSES ---------------- #
greetings = ["Hello!", "Hey there!", "Hi!", "Assalam o Alaikum!"]
smalltalk = ["I'm doing great", "All good here!", "Feeling smart today"]
jokes = [
    "Why do programmers hate nature? Too many bugs",
    "Why did the computer go to therapy? It had too many bytes",
    "I told my computer a joke... it didn’t laugh"
]

sad_words = ["sad", "depressed", "tired", "upset"]
happy_words = ["happy", "good", "great", "awesome"]

# ---------------- TYPING EFFECT ---------------- #
def typing(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.02)
    print()

# ---------------- CHAT FUNCTION ---------------- #
def chatbot_response(user_input):
    global user_name
    user_input = user_input.lower().strip()

    # Commands
    if user_input == "/help":
        return "Commands: /help, /clear, exit"

    elif user_input == "/clear":
        return "Chat cleared (not really, just for fun 😄)"

    # Greeting
    if re.search(r"\b(hi|hello|hey)\b", user_input):
        return random.choice(greetings)

    # Name memory
    elif "my name is" in user_input:
        user_name = user_input.split("my name is")[-1].strip()
        return f"Nice to meet you, {user_name}"

    elif "your name" in user_input:
        return "I'm your advanced chatbot"

    # Mood detection
    elif any(word in user_input for word in sad_words):
        return "I'm here for you. Things will get better."

    elif any(word in user_input for word in happy_words):
        return "That's great to hear!"

    # Small talk
    elif "how are you" in user_input:
        return random.choice(smalltalk)

    # Time & Date
    elif "time" in user_input:
        return "Current time: " + datetime.now().strftime("%H:%M:%S")

    elif "date" in user_input:
        return "Today's date: " + datetime.now().strftime("%d-%m-%Y")

    # Joke
    elif "joke" in user_input:
        return random.choice(jokes)

    # Knowledge base
    for key in knowledge_base:
        if key in user_input:
            return knowledge_base[key]

    # Default
    if user_name:
        return f"{user_name}, I didn't understand that"
    return "I didn't understand that"

# ---------------- MAIN ---------------- #
def main():
    print("\nChatbot: Hello! Type 'exit' to quit.\n")

    with open("chat_log.txt", "a") as log:
        while True:
            user_input = input("You: ")

            # Exit confirmation
            if user_input.lower() == "exit":
                confirm = input("Are you sure? (yes/no): ")
                if confirm.lower() == "yes":
                    typing("Chatbot: Goodbye!")
                    break
                else:
                    continue

            bot_reply = chatbot_response(user_input)

            print("Chatbot: ", end="")
            typing(bot_reply)

            # Save log
            log.write(f"{datetime.now()} - You: {user_input}\n")
            log.write(f"{datetime.now()} - Bot: {bot_reply}\n")

if __name__ == "__main__":
    main()