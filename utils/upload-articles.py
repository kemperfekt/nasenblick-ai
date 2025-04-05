import os
import weaviate
from dotenv import load_dotenv

# 📌 Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")  # Get OpenAI API Key from .env
weaviate_url = os.getenv("WEAVIATE_URL")  # Get Weaviate URL from .env
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")  # Get Weaviate API Key from .env

# Ensure the OpenAI API Key is set correctly
if not openai_api_key:
    raise ValueError("OpenAI API Key not found in .env file")

# Connect to Weaviate using the API Key for authentication
client = weaviate.Client(
    url=weaviate_url,
    auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),  # Authentication with Weaviate API key
    additional_headers={"X-OpenAI-Api-Key": openai_api_key}  # Pass OpenAI API key for vectorization
)

# Manually create a list of articles with just title and content
articles = [
    {
        "title": "Bellen bei Hunden",
        "content": "Bellen ist ein natürliches Verhalten für Hunde. Es kann aus verschiedenen Gründen auftreten, z.B. um sich zu verteidigen oder auf ein Geräusch zu reagieren."
    },
    {
        "title": "Alleinbleiben",
        "content": "Hunde können Schwierigkeiten beim Alleinbleiben haben. Es ist wichtig, diese Fähigkeit schrittweise zu trainieren, um Trennungsangst zu vermeiden."
    },
    {
        "title": "Hundetraining mit positiven Verstärkern",
        "content": "Positives Verstärken ist eine der effektivsten Methoden im Hundetraining. Es geht darum, gutes Verhalten zu belohnen, um es zu verstärken."
    },
]

# Function to insert articles into Weaviate
def insert_article(title, content):
    # Create a document to insert into Weaviate
    article_data = {
        "title": title,
        "content": content
    }

    # Add the article to Weaviate under the "Article" class
    client.data_object.create(
        data_object=article_data,
        class_name="Article"
    )
    print(f"Article '{title}' inserted successfully.")

# Insert all articles from the list
def insert_articles():
    for article in articles:
        insert_article(
            title=article["title"],
            content=article["content"]
        )

if __name__ == "__main__":
    insert_articles()
