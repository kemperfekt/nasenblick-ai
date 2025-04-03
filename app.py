import streamlit as st
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Kemperfekt KI-Coach", page_icon="🐾")
st.title("🐶 Kemperfekt KI-Coach")

llm = OpenAI(temperature=0.3, model="gpt-4")
service_context = ServiceContext.from_defaults(llm=llm)

with st.spinner("Lade Wissensbasis..."):
    reader = SimpleDirectoryReader("content")
    docs = reader.load_data()
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    query_engine = index.as_query_engine()

st.markdown("Stelle deine Frage rund um Hundeverhalten oder Training:")
user_input = st.text_input("Deine Frage", placeholder="Mein Hund bellt, wenn es klingelt ...")

if user_input:
    with st.spinner("Formuliere Antwort..."):
        response = query_engine.query(user_input)
        st.markdown("---")
        st.markdown("**Antwort:**")
        st.write(response.response)
        st.markdown("---")
        st.caption("Hinweis: Diese Antwort basiert auf den Inhalten von kemperfekt.")
