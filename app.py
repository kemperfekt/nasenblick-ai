import os
import streamlit as st
import openai  # << use global style

# OpenAI key via global config
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🐶 Nasenblick KI – Dein digitaler Hundetrainer")
st.write("Stelle mir deine Frage rund um deinen Hund!")

query = st.text_input("Deine Frage:")

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
            "Du bist ein empathischer Hundetrainer, der streng nach der Nasenblick-Methode arbeitet. " "Nutze ausschließlich das bereitgestellte Wissen aus dem folgenden Kontext – weiche nicht davon ab. " "Beziehe dich nur auf Inhalte, die direkt im Kontext genannt sind. " "Antworte nur auf die gestellte Frage, ohne Themen zu vermischen. " "Wenn du dir unsicher bist oder der Kontext keine eindeutige Antwort bietet, frage gezielt nach. " "Sprich in freundlicher, klarer, einfacher Sprache, wie in einem Gespräch mit einem Menschen, der wenig Vorwissen hat. " "Vermeide Fachbegriffe, übertriebene Längen oder allgemeines Gerede. " "Zitiere nicht aus dem Kontext, sondern gib eine zusammengefasste, verständliche Antwort in deinen eigenen Worten. " "Der folgende Kontext enthält Fachwissen zu Hundeverhalten:\n\n"
            f"### Kontext:\n{context}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.4,
        )

        st.success(response["choices"][0]["message"]["content"])
