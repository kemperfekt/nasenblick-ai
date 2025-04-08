import os
import streamlit as st
from openai import OpenAI

# 📌 Setze deinen OpenAI-Key über Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# UI
st.title("🐶 Nasenblick KI")
st.write("Stelle deine Frage rund um Hundeverhalten:")

query = st.text_input("Deine Frage:")

client = OpenAI()

# Button to trigger the response generation
if st.button('Get Answer'):
    if query:  # Ensure user query is not empty
        # Pass the user input to the OpenAI responses.create function
        response = client.responses.create(
            model="gpt-4",  # You can replace this with the correct model you're using
            input=query  # The user input
        )
        
        # Get the output text from the response
        answer = response['choices'][0]['text'].strip()
        
        # Display the response to the user
        st.write("Answer:", answer)
    else:
        st.write("Please enter a question.")