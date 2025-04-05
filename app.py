    import os
    import streamlit as st
    from dotenv import load_dotenv
    import weaviate
    import openai

    # 📌 Load environment variables from .env file
    load_dotenv()  # This will load variables from .env file into environment
    openai_api_key = os.getenv("OPENAI_API_KEY")  # Get OpenAI API Key from .env
    weaviate_url = os.getenv("WEAVIATE_URL")  # Get Weaviate URL from .env

    # UI
    st.title("🐶 Nasenblick KI")
    st.write("Hier findest Du Hilfe bei der Erziehung Deines Hundes:")

    query = st.text_input("Wie lautet Dein Anliegen:")

    # Setup Weaviate Client
    client = weaviate.Client(url=weaviate_url)  # Connect to your Weaviate instance

    # Retrieve articles from Weaviate
    def query_weaviate(query):
        # Perform a query to Weaviate to find relevant articles
        try:
            result = client.query.get('Article').with_near_text({
                'concepts': [query]
            }).with_limit(3).do()  # Limit to top 3 relevant articles
            return result
        except Exception as e:
            st.error(f"Fehler bei der Anfrage an Weaviate: {str(e)}")
            return None

    # Function to interact with OpenAI API for answering
    def get_openai_answer(query, context):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",  # or another model of your choice
                prompt=f"Use the following context to answer the question: {context}\n\nQuestion: {query}",
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            st.error(f"Fehler bei der Anfrage an OpenAI: {str(e)}")
            return "Es gab ein Problem mit der Antwort von OpenAI."

    if query:
        with st.spinner("Ich denke nach..."):
            # Query Weaviate for relevant content
            weaviate_result = query_weaviate(query)
            if weaviate_result:
                # Extract content from the Weaviate result if available
                context = "\n".join([doc['content'] for doc in weaviate_result['data']['Get']['Article']])  # Assuming the content field exists

                # Get the response from OpenAI
                answer = get_openai_answer(query, context)
                st.success(answer)

                # Optional: Show retrieved documents for transparency
                with st.expander("🔎 Verwendete Wissensabschnitte"):
                    for doc in weaviate_result['data']['Get']['Article']:
                        st.markdown(f"• {doc['title']}")
                        st.text(doc['content'][:500] + "...")
            else:
                st.warning("Keine relevanten Artikel gefunden.")