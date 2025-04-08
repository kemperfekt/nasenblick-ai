import os, json
import streamlit as st
from dotenv import load_dotenv
import weaviate
#from weaviate.auth import AuthApiKey
from weaviate.classes.init import Auth
import openai


# 📌 Load environment variables from .env file
load_dotenv()  # This will load variables from .env file into environment
openai_api_key = os.getenv("OPENAI_API_KEY")  # Get OpenAI API Key from .env
weaviate_url = os.getenv("WEAVIATE_URL")  # Get Weaviate URL from .env
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")  # Get Weaviate API Key from .env

# UI
st.title("🐶 Nasenblick KI")
st.write("Hier findest Du Hilfe bei der Erziehung Deines Hundes:")

query = st.text_input("Wie lautet Dein Anliegen?")
#context = "Empathischer Hundetrainer mit ruhiger Stimme"


# Connect to Weaviate Cloud using the API key
#client = weaviate.connect_to_weaviate_cloud(
#    cluster_url=weaviate_url,
#    auth_credentials=AuthApiKey(weaviate_api_key),
#    headers={
#        "X-Openai-Api-Key": openai_api_key  # Add the OpenAI API key explicitly for vectorization
#   }
#)

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
    headers={
        "X-Openai-Api-Key": openai_api_key  # Add the OpenAI API key explicitly for vectorization
   }
)

# Check if the connection is working
if client.is_ready():
    st.success("Connected to Weaviate successfully!")

# Retrieve articles from Weaviate (make sure collection name is correct)
    def query_weaviate(query):
        collection = client.collections.get("Article")

        result = collection.query.near_text(
        query=query,
        limit=2
        )
        
        # Check if result is valid
        if not result.objects:
            return []
        
        # Extract 'title' and 'content' from each article object
        articles = []
        for obj in result.objects:
            articles.append({
                'title': obj['properties'].get('title', ''),
                'content': obj['properties'].get('content', '')
            })

        return articles


        #return result.objects
    #for obj in result.objects:
    #    st.write((json.dumps(obj.properties, indent=2)))


# Function to interact with OpenAI API for answering
def get_openai_answer(query, context):
    # Set the OpenAI API key
    openai.api_key=openai_api_key

    # Use the Completion API
    response = openai.Completion.create(
        model="gpt-4",  # For GPT-3.5 or GPT-4, you can use different models as needed
        prompt=f"Context: {context}\n\nQuestion: {query}",
        max_tokens=150
    )
    
    # Return the text response from the model
    return response['choices'][0]['text'].strip()

if query:
    st.write("Query:", query)
    with st.spinner("Ich denke nach..."):
        # Query Weaviate for relevant content
        weaviate_result = query_weaviate(query)
        st.write("weaviate_result:", weaviate_result)

        # Log the raw Weaviate result to debug
        st.write(weaviate_result)  # This will show the raw result from Weaviate for debugging
        

        if weaviate_result and 'data' in weaviate_result and 'Get' in weaviate_result['data'] and 'Article' in weaviate_result['data']['Get']:
            # Assuming your Weaviate data structure is correct, adjust 'content' if necessary
            context = "\n".join([doc['content'] for doc in weaviate_result['data']['Get']['Article']])

            # Get the response from OpenAI
            answer = get_openai_answer(query, context)
            st.success(answer)

        else:
            st.warning("Keine relevanten Artikel gefunden. Bitte versuche es mit einer anderen Anfrage.")

client.close()