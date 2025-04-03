import os
import nltk
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.openai import OpenAI

# Ensure the 'punkt' tokenizer is available
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_path)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=nltk_data_path)

# Check for OpenAI API key in Streamlit secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.warning("⚠️ Kein OpenAI API-Key gefunden. Bitte .streamlit/secrets.toml einrichten.")
else:
    # Initialize the OpenAI LLM with the API key from secrets
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.7)
    service_context = ServiceContext.from_defaults(llm=llm)

    # Streamlit UI setup
    st.title("🐶 Nasenblick KI")
    st.write("Stelle mir deine Frage zur Hundeerziehung!")

    query = st.text_input("Was möchtest du wissen?")
    if query:
        with st.spinner("Denke nach..."):
            # Load documents from the 'data' directory
            documents = SimpleDirectoryReader("data").load_data()
            # Create a vector store index from the documents
            index = VectorStoreIndex.from_documents(documents, service_context=service_context)
            # Query the index with the user's input
            response = index.query(query)
            # Display the response
            st.success(response.response)
