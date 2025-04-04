import os
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title("🐶 Nasenblick KI – Dein digitaler Hundetrainer")
st.write("Stelle mir deine Frage rund um deinen Hund!")

query = st.text_input("Deine Frage:")

SYSTEM_PROMPT = """Du bist ein empathischer Hundetrainer, der nach der Nasenblick-Methode arbeitet.
Nutze vorrangig das bereitgestellte Wissen aus dem folgenden Kontext.
Antworte ruhig, freundlich, empathisch und in einfacher Sprache.
Frage nach und reformuliere, um dein Verständnis abzusichern.
Vermeide Fachbegriffe und gib keine langen Artikel wieder.
Antworte nur auf die gestellte Frage und fasse dich kurz, wie in einem persönlichen Gespräch."""

prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

@st.cache_resource
def load_vectorstore():
    loader = DirectoryLoader("content", glob="*.md")
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.split_documents(raw_docs)

    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)

if query:
    with st.spinner("Ich denke nach..."):
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever()

        qa_chain = RetrievalQA.from_chain_type(
            llm = OpenAI(temperature=0.7),
            retriever=retriever,
            chain_type="stuff"
        )

        response = qa_chain.run(query)
        st.success(response)
