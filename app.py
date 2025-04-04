import os
import streamlit as st
import nltk

# Download punkt if needed
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_path)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=nltk_data_path)

from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI

# Use Streamlit secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found in .streamlit/secrets.toml")
    st.stop()

llm = OpenAI(api_key=openai_api_key, temperature=0.7)
service_context = ServiceContext.from_defaults(llm=llm)

# UI
st.title("🐶 Nasenblick KI")
query = st.text_input("Frage zur Hundeerziehung:")

if query:
    with st.spinner("Suche nach Antwort..."):
        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        response = index.query(query)
        st.success(response.response)
