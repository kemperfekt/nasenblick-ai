import streamlit as st
from openai import OpenAI

# Setup
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit UI
st.title("🐶 Nasenblick KI")
st.write("Stelle mir deine Frage zur Hundeerziehung!")

query = st.text_input("Was möchtest du wissen?")

if query:
    with st.spinner("Denke nach..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du bist ein erfahrener Hundetrainer."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
        )
        st.success(response.choices[0].message.content)
