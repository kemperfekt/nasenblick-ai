import os
import streamlit as st
from openai import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA

# OpenAI-Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit-UI
st.title("🐶 Nasenblick KI – Dein digitaler Hundetrainer")
st.write("Stelle mir deine Frage rund um deinen Hund!")

query = st.text_input("Deine Frage:")

# Daten vorbereiten (nur beim ersten Start nötig, Cache möglich)
@st.cache_resource
def load_knowledge_base():
    docs = []
    loader = TextLoader("content", glob="*.md", autodetect_encoding=True)
    raw_docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.split_documents(raw_docs)

    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding)

    return vectorstore

if query:
    with st.spinner("Ich denke nach..."):
        vectorstore = load_knowledge_base()
        retriever = vectorstore.as_retriever()

        qa = RetrievalQA.from_chain_type(
            llm=client.chat.completions,
