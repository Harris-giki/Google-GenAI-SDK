# agent.py
import re
import json
import os
import google.generativeai as genai
from db import get_user_by_id, update_user_email

# Step 1: Set up Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBto28XTxcOE310z5th_8tgWRq2P8ty4Fg"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Step 2: Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 3: Classify + handle prompt
def classify_and_respond(prompt: str):
    classify_prompt = f"""
You are an AI agent. Your job is to classify the following user request into one of two categories:

1. 'database' – if the user is trying to access, update, or interact with the database
2. 'general' – if it's a question or something that doesn't require accessing the database

Also extract any required parameters (like user ID or email) if it's a database request.

Example format:
Category: database
Function: get_user_by_id
Arguments: {{ "user_id": 5 }}

Now classify:
User: "{prompt}"
"""

    response = model.generate_content(classify_prompt).text
    print("LLM Classification Output:")
    print(response)

    if "database" in response:
        # Extract JSON part from the "Arguments" line
        match = re.search(r"Arguments:\s*(\{.*\})", response)
        if match:
            try:
                args = json.loads(match.group(1))
            except json.JSONDecodeError:
                return "Couldn't parse arguments."

            if "get_user_by_id" in response:
                return get_user_by_id(args.get("user_id"))

            elif "update_user_email" in response:
                return update_user_email(args.get("user_id"), args.get("new_email"))


    return model.generate_content(prompt).text

# Step 4: Run interaction loop (CLI mode)
if __name__ == "__main__":
    while True:
        prompt = input("\nYou: ")
        if prompt.lower() in ['exit', 'quit']:
            break
        result = classify_and_respond(prompt)
        print("Agent:", result)
