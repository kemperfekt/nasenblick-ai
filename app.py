import os
import nltk
import streamlit as st
import openai

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Ensure nltk tokenizer data is available
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=nltk_data_path)

# UI
st.title("🐶 Nasenblick KI")
st.write("Stelle mir deine Frage zur Hundeerziehung!")

query = st.text_input("Was möchtest du wissen?")

# Only proceed if user entered a question
if query:
    with st.spinner("Denke nach..."):

        # Load documents
        documents = SimpleDirectoryReader("data").load_data()

        # Define LLM and embedding model
        llm = OpenAI(temperature=0.7)
        embed_model = OpenAIEmbedding(model="text-embedding-3-small")

        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model
        )

        # Build index
        index = VectorStoreIndex.from_documents(
            documents, service_context=service_context
        )

        # Query index
        response = index.query(query)

        # Show result
        st.success(response.response)