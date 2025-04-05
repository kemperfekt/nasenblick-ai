import os
import streamlit as st
from dotenv import load_dotenv
import weaviate
import openai
from weaviate.auth import AuthApiKey

# 📌 Load environment variables from .env file
load_dotenv()  # This will load variables from .env file into environment
openai_api_key = os.getenv("OPENAI_API_KEY")  # Get OpenAI API Key from .env
print(f"Loaded OpenAI API Key: {openai_api_key}")
weaviate_url = os.getenv("WEAVIATE_URL")  # Get Weaviate URL from .env
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")  # Get Weaviate API Key from .env

# UI
st.title("🐶 Nasenblick KI")
st.write("Hier findest Du Hilfe bei der Erziehung Deines Hundes:")

query = st.text_input("Wie lautet Dein Anliegen:")

# Connect to Weaviate Cloud using the API key
client = weaviate.Client(
    url=weaviate_url,
    auth_client_secret=AuthApiKey(api_key=weaviate_api_key),
    additional_headers={
        "X-Openai-Api-Key": openai_api_key  # Add the OpenAI API key explicitly for vectorization
    }
)

# Check if the connection is working
if client.is_ready():
    st.success("Weaviate connected successfully!")

# Retrieve articles from Weaviate (make sure collection name is correct)
def query_weaviate(query):
    # Perform a query to Weaviate to find relevant articles
    result = client.query.get("Article", ["title", "content"])  # Get the fields you want to retrieve
    result = result.with_near_text({
        'concepts': [query]
    }).with_limit(3).do()  # Limit to top 3 relevant articles

    return result

# Function to interact with OpenAI API for answering
def get_openai_answer(query, context):
    response = openai.Completion.create(
        model="text-davinci-003",  # or another model of your choice
        prompt=f"Use the following context to answer the question: {context}\n\nQuestion: {query}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

if query:
    with st.spinner("Ich denke nach..."):
        # Query Weaviate for relevant content
        weaviate_result = query_weaviate(query)

        # Log the raw Weaviate result to debug
        st.write(weaviate_result)  # This will show the raw result from Weaviate for debugging

        # Check if the result contains any data
        if weaviate_result and 'data' in weaviate_result and 'Get' in weaviate_result['data'] and 'Article' in weaviate_result['data']['Get']:
            # Assuming your Weaviate data structure is correct, adjust 'content' if necessary
            context = "\n".join([doc['content'] for doc in weaviate_result['data']['Get']['Article']])

            # Get the response from OpenAI
            answer = get_openai_answer(query, context)
            st.success(answer)

            # Optional: Show retrieved documents for transparency
            with st.expander("🔎 Verwendete Wissensabschnitte"):
                for doc in weaviate_result['data']['Get']['Article']:
                    st.markdown(f"• {doc['title']}")
                    st.text(doc['content'][:500] + "...")
        else:
            st.warning("Keine relevanten Artikel gefunden. Bitte versuche es mit einer anderen Anfrage.")
