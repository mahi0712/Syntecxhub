from flask import Flask, request, jsonify
from chatbot import chatbot_response  # tumhara existing function

app = Flask(__name__)

@app.route("/")
def home():
    return "Chatbot is LIVE!"

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    
    reply = chatbot_response(user_msg)

    # save log
    with open("chat_log.txt", "a") as f:
        f.write(f"User: {user_msg} | Bot: {reply}\n")

    return jsonify({"reply": reply})

app.run(host="0.0.0.0", port=10000)