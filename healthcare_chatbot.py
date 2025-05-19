
import tkinter as tk
from tkinter import scrolledtext
import spacy
import random

# Load spaCy English NLP model
nlp = spacy.load("en_core_web_sm")

# Symptom to condition response map
symptom_condition_map = {
    "fever": "You might have an infection or the flu. Monitor your temperature and stay hydrated.",
    "cough": "Persistent coughs may indicate respiratory infections. Rest and see a doctor if it continues.",
    "headache": "This could be due to stress, dehydration, or vision problems. Try to rest and drink water.",
    "chest pain": "This might be serious. If it persists or is severe, seek emergency care immediately.",
    "fatigue": "Could be caused by stress, lack of sleep, or a vitamin deficiency. Get enough rest.",
    "shortness of breath": "This may indicate an issue with the lungs or heart. Please consult a physician."
}

# Simulate IoT health data
def get_simulated_iot_data():
    return {
        "heart_rate": random.randint(60, 120),
        "temperature": round(random.uniform(97.0, 103.0), 1),
        "steps_today": random.randint(1000, 10000)
    }

# Analyze IoT data and return suggestions
def interpret_iot_data(data):
    messages = []
    if data["heart_rate"] > 100:
        messages.append("Your heart rate is elevated. Are you feeling stressed or anxious?")
    if data["temperature"] > 100.4:
        messages.append("Your temperature is above normal. You may have a fever.")
    if data["steps_today"] < 2000:
        messages.append("You've taken fewer steps today. Try to stay more active.")
    return messages if messages else ["Your vital signs are within a normal range."]

# Use NLP to extract symptoms from user input
def extract_symptom(user_input):
    doc = nlp(user_input.lower())
    matches = [symptom_condition_map[token.lemma_] for token in doc if token.lemma_ in symptom_condition_map]
    return "\n".join(set(matches)) if matches else "I'm sorry, I couldn't identify your symptoms. Could you describe it differently?"

# Send button handler
def send_message():
    user_input = entry.get()
    chatbox.insert(tk.END, f"You: {user_input}\n")
    entry.delete(0, tk.END)

    if user_input.lower() in ["exit", "quit", "bye"]:
        chatbox.insert(tk.END, "Bot: Take care! Goodbye.\n")
        return
    elif user_input.lower() == "iot":
        data = get_simulated_iot_data()
        chatbox.insert(tk.END, f"Bot: IoT Health Data:\n  Heart Rate: {data['heart_rate']} bpm\n  Temperature: {data['temperature']} °F\n  Steps Today: {data['steps_today']} steps\n")
        for msg in interpret_iot_data(data):
            chatbox.insert(tk.END, f"Bot: {msg}\n")
    else:
        response = extract_symptom(user_input)
        chatbox.insert(tk.END, f"Bot: {response}\n")

# GUI Setup
window = tk.Tk()
window.title("AI Healthcare Chatbot")
window.geometry("520x450")

chatbox = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20, font=("Arial", 10))
chatbox.pack(pady=10)

entry = tk.Entry(window, width=50, font=("Arial", 12))
entry.pack(pady=5)

send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

chatbox.insert(tk.END, "Bot: Hello! Describe your symptoms, type 'iot' for health data, or 'bye' to exit.\n")

window.mainloop()
