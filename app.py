import os
import nltk
import streamlit as st

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Ensure NLTK data is available
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=nltk_data_path)

# Setup OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"]

# UI
st.title("🐶 Nasenblick KI")
st.write("Stelle mir deine Frage zur Hundeerziehung!")

query = st.text_input("Was möchtest du wissen?")

if query:
    with st.spinner("Denke nach..."):
        # Load documents
        documents = SimpleDirectoryReader("data").load_data()

        # Explicitly configure LLM and embedding with API key
        llm = OpenAI(api_key=api_key, temperature=0.7)
        embed_model = OpenAIEmbedding(api_key=api_key, model="text-embedding-3-small")

        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model
        )

        # Build index and query
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        response = index.query(query)

        st.success(response.response)