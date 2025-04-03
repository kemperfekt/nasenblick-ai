import nltk
import os

# Stelle sicher, dass punkt an einem beschreibbaren Ort liegt
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_path)

# Nur wenn nötig downloaden (um es nicht jedes Mal zu versuchen)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=nltk_data_path)

import streamlit as st
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.openai import OpenAI

# API-Key aus Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🐶 Nasenblick KI")
st.write("Stelle mir deine Frage zur Hundeerziehung!")

query = st.text_input("Was möchtest du wissen?")

if query:
    with st.spinner("Denke nach..."):
        # Dummy: Nur statische Daten lesen (du kannst das später mit deinen .md-Dateien erweitern)
        documents = SimpleDirectoryReader("data").load_data()

        from llama_index.embeddings.openai import OpenAIEmbedding

        # Erstelle dein Embedding-Modell mit API-Key (aus st.secrets)
        embed_model = OpenAIEmbedding(api_key=st.secrets["OPENAI_API_KEY"])

        # Service Context inkl. Embedding und LLM
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(temperature=0.7, api_key=st.secrets["OPENAI_API_KEY"]),
            embed_model=embed_model
        )
        # 🔍 Index erstellen
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        response = index.query(query)
        st.success(response.response)
        
    service_context = ServiceContext.from_defaults(llm=OpenAI(temperature=0.7))
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        response = index.query(query)
        st.success(response.response)
