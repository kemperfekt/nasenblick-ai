import streamlit as st
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI

# API-Key aus Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🐶 Nasenblick KI")
st.write("Stelle mir deine Frage zur Hundeerziehung!")

query = st.text_input("Was möchtest du wissen?")

if query:
    with st.spinner("Denke nach..."):
        # Dummy: Nur statische Daten lesen (du kannst das später mit deinen .md-Dateien erweitern)
        documents = SimpleDirectoryReader("data").load_data()

        service_context = ServiceContext.from_defaults(llm=OpenAI(temperature=0.7))
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        response = index.query(query)
        st.success(response.response)
