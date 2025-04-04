import os
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate  # ✅ Wichtig für korrekten Prompt

# 📌 Setze deinen OpenAI-Key über Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# UI
st.title("🐶 Nasenblick KI")
st.write("Stelle deine Frage rund um Hundeverhalten:")

query = st.text_input("Deine Frage:")

# Wissen vorbereiten
@st.cache_resource
def load_vectorstore():
    loader = DirectoryLoader("content", glob="*.md")
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.split_documents(raw_docs)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore

if query:
    with st.spinner("Ich denke nach..."):
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever()

        # 💡 SYSTEM PROMPT
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
Du bist ein empathischer Hundetrainer, der nach der Nasenblick-Methode arbeitet.
Nutze ausschließlich das bereitgestellte Wissen aus dem folgenden Kontext, um die Frage zu beantworten.

Kontext:
{context}

Frage:
{question}

Antworte ruhig, einfach, empathisch und auf den Punkt. Sprich wie in einem Gespräch, nicht wie in einem Artikel.
"""
        )

        llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.3)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

        result = qa_chain.run(query)
        st.success(result["result"])

        # Optional: Zeige verwendete Inhalte (Debug/Transparenz)
        with st.expander("🔎 Verwendete Wissensabschnitte"):
            for doc in result["source_documents"]:
                st.markdown(f"• {doc.metadata['source']}")
                st.text(doc.page_content[:500] + "...")
