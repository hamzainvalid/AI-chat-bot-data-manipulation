import pandas as pd
from google import genai

malfunction = ''
issue = ''
symptom = ''
history = []
cols = []

API_KEY = 'key'

client = genai.Client(api_key=API_KEY)

def load_csv(file_path):
    global malfunction
    global issue
    global symptom
    global cols
    try:
        df = pd.read_csv(file_path)

        #print("\n--- Full CSV Data ---")
        cols = df[["Malfunction_Name", "Issue", "Symptom"]]
        #print(df.to_string(index=False))  # to_string prints the entire DataFrame without truncating
        #print(df["Symptom"])
        #print(df.columns)

        malfunction = df["Malfunction_Name"]
        issue = df["Issue"]
        symptom = df["Symptom"]

        return df

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def chat_with_gemini(user_message, history):
    support_knowledge = cols
    conversation_text = "\n".join(
        [f"User: {msg['user']}\nBot: {msg['bot']}" for msg in history]
    )

    prompt = f"""
    You are a friendly customer support assistant.
    You help classify customer requests into ISSUE, MALFUNCTION, or SYMPTOM.
    You have the following knowledge base:
    
    {support_knowledge}
    
    Conversation so far:
    {conversation_text}
    
    Customer says: {user_message}
    
    Reply naturally, and ask clarifying questions until you can confidently classify.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

if __name__ == "__main__":
    df = load_csv("malfunctions.csv")

    print("🤖 Support Bot: Hi! I’m here to help. Tell me what’s going on.")
    history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "bye", "exit"]:
            print("🤖 Support Bot: Goodbye!")
            break

        bot_reply = chat_with_gemini(user_input, history)
        print(f"🤖 Support Bot: {bot_reply}")

        history.append({"user": user_input, "bot": bot_reply})
