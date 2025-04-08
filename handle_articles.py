import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv
import os

# 📌 Load environment variables from .env file
load_dotenv()  # This will load variables from .env file into environment
weaviate_url = os.getenv("WEAVIATE_URL")  # Get Weaviate URL from .env
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")  # Get Weaviate API Key from .env

# Connect to Weaviate Client
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key)
)

# Function to delete all articles in the collection
# Function to delete all articles in the collection
def delete_all_articles():
    # Query to get all objects in the "Article" class
    result = client.query.get("Article", ["_id"]).with_limit(1000).do()  # Limiting to 1000 articles, adjust as needed

    # Check if the result contains the expected data
    if 'data' in result and 'Get' in result['data'] and 'Article' in result['data']['Get']:
        # Get the UUIDs of all articles
        article_uuids = [obj['_id'] for obj in result['data']['Get']['Article']]
        
        if article_uuids:
            # Perform batch delete for each article
            with client.batch as batch:
                for uuid in article_uuids:
                    batch.delete("Article", uuid)
            print(f"Deleted {len(article_uuids)} articles.")
        else:
            print("No articles found to delete.")
    else:
        print("No articles to delete in the 'Article' class.")


# Function to add new articles
def create_new_articles():
    # Define new articles
    new_articles = [
        {"title": "Article 1", "content": "Content for article 1."},
        #{"title": "Article 2", "content": "Content for article 2."},
        #{"title": "Article 3", "content": "Content for article 3."},
        #{"title": "Article 4", "content": "Content for article 4."},
        #{"title": "Article 5", "content": "Content for article 5."},
        #{"title": "Article 6", "content": "Content for article 6."},
        #{"title": "Article 7", "content": "Content for article 7."},
        #{"title": "Article 8", "content": "Content for article 8."},
        #{"title": "Article 9", "content": "Content for article 9."},
        #{"title": "Article 10", "content": "Content for article 10."}
    ]

    # Add new articles to Weaviate
    for article in new_articles:
        client.data_object.create(
            data_object=article,
            class_name="Article"
        )
        print(f"Created article: {article['title']}")

# Deleting all articles and creating new ones
delete_all_articles()
#create_new_articles()
client.close()
