import os
import streamlit as st
from openai import OpenAI

# OpenAI-Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit-UI
st.title("🐶 Nasenblick KI – Dein digitaler Hundetrainer")
st.write("Stelle mir deine Frage rund um deinen Hund!")

query = st.text_input("Deine Frage:")

# Hilfsfunktion: Inhalte laden aus content/*.md
def load_training_content():
    content = ""
    content_dir = "content"
    for filename in os.listdir(content_dir):
        if filename.endswith(".md"):
            with open(os.path.join(content_dir, filename), "r", encoding="utf-8") as f:
                content += f.read() + "\n\n"
    return content

if query:
    with st.spinner("Ich denke nach..."):
        context = load_training_content()

        system_prompt = (
            "Du bist ein erfahrener Hundetrainer, der nach der Nasenblick-Methode arbeitet. "
            "Nutze ausschließlich das bereitgestellte Hintergrundwissen aus dem folgenden Kontext. "
            "Erfinde keine Informationen, antworte ehrlich, wenn du etwas nicht weißt.\n\n"
            f"### Kontext:\n{context}"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.4,
        )

        st.success(response.choices[0].message.content)
