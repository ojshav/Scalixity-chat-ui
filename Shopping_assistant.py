import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import psycopg2
from psycopg2.extras import DictCursor
import time
import psutil
from langchain.callbacks.tracers import LangChainTracer
from langchain.callbacks.manager import CallbackManager
from langsmith import Client
from langchain.embeddings import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load environment variables first
load_dotenv()

# Environment variables setup
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "Ecommerce"

POSTGRES_URL = os.getenv("POSTGRES_URL")

# Initialize LangChain tracer
tracer = LangChainTracer()
callback_manager = CallbackManager([tracer])

# Initialize LangSmith client
client = Client()

# Initialize Ollama LLM with callbacks
llm = Ollama(
    model="mistral",
    temperature=0.7,
    callback_manager=callback_manager
)

def get_db_connection():
    try:
        return psycopg2.connect(POSTGRES_URL)
    except psycopg2.Error as e:
        raise Exception(f"Database connection failed: {str(e)}")

def get_available_categories():
    """Get all available categories from the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT category FROM products")
        categories = [row[0] for row in cur.fetchall()]
        return sorted(list(set(categories)))
    except Exception as e:
        print(f"Error fetching categories: {str(e)}")
        return []  # Return an empty list on error
    finally:
        cur.close()
        conn.close()

def normalize_category_with_llm(category_input, available_categories):
    """Use LLM to handle category normalization."""
    if category_input.lower() in [c.lower() for c in available_categories]:
        return category_input  # Return directly if it matches any category

    prompt = (
        "You are an expert shopping assistant. Normalize the following input to match one of "
        f"the available categories: {available_categories}. Input: '{category_input}'"
    )
    response = llm.invoke(prompt)
    normalized_category = response.strip()
    if normalized_category.lower() in [c.lower() for c in available_categories]:
        return normalized_category

    return None

def get_available_sizes_for_category(category):
    """Fetch available sizes for a given category from the database."""
    if not category:  # Check for empty category
        return []

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    try:
        cur.execute(""" 
            SELECT DISTINCT product_size 
            FROM products 
            WHERE LOWER(category) = LOWER(%s)
            ORDER BY product_size
        """, (category,))
        sizes = [row['product_size'] for row in cur.fetchall()]
        return sorted(list(set(sizes)))
    except Exception as e:
        print(f"Error fetching sizes for category '{category}': {str(e)}")
        return []  # Return an empty list on error
    finally:
        cur.close()
        conn.close()

def get_available_colors_for_category_and_size(category, size):
    """Fetch available colors for a given category and size."""
    if not category or not size:  # Check for empty category or size
        return []

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    try:
        cur.execute(""" 
            SELECT DISTINCT product_color 
            FROM products 
            WHERE LOWER(category) = LOWER(%s)
            AND LOWER(product_size) = LOWER(%s)
            ORDER BY product_color
        """, (category, size))
        colors = [row['product_color'] for row in cur.fetchall()]
        return sorted(list(set(colors)))
    except Exception as e:
        print(f"Error fetching colors for category '{category}' and size '{size}': {str(e)}")
        return []  # Return an empty list on error
    finally:
        cur.close()
        conn.close()

def generate_product_recommendation(product):
    """Generate a short recommendation for the given product using LLM."""
    prompt = (
        f"You are a shopping assistant. Provide a brief reason to buy the following product: "
        f"{product['product_name']} by {product['product_company_name']}. "
        f"Keep it concise."
    )
    response = llm(prompt)
    return response.strip()

def find_products_by_criteria(category, size, color):
    """Find products matching the given criteria."""
    if not category or not size or not color:  # Check for empty inputs
        return []

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    try:
        cur.execute(""" 
            SELECT * FROM products 
            WHERE LOWER(category) = LOWER(%s)
            AND LOWER(product_size) = LOWER(%s)
            AND LOWER(product_color) = LOWER(%s)
            ORDER BY product_name
            LIMIT 5
        """, (category, size, color))
        return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        print(f"Error finding products: {str(e)}")
        return []  # Return an empty list on error
    finally:
        cur.close()
        conn.close()

def chat_with_assistant():
    """Interactive chat function with more natural conversation flow."""
    print("Hi! 👋 I'm your personal shopping assistant. I'm here to help you find the perfect item!")

    available_categories = get_available_categories()
    categories_list = ", ".join(available_categories)  # Prepare the categories for display
    print("\nI can help you find these types of products:")
    print(categories_list)

    while True:
        print("\nWhat are you looking for today? (or type 'quit' to end our chat)")
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("It was great helping you today! Come back anytime! 👋")
            break

        if not user_input:
            print("I didn't catch that. Could you please tell me what you're looking for?")
            continue

        # Normalize category input using LLM
        category = normalize_category_with_llm(user_input, available_categories)
        if not category:
            print(f"Hmm... I couldn't match '{user_input}' to any of our categories. 🤔")
            print("Here's what I can help you find:", categories_list)
            continue

        # Get and present size options
        available_sizes = get_available_sizes_for_category(category)
        if not available_sizes:
            print(f"I'm sorry, but I don't have any {category} items in stock right now. 😔")
            print("Would you like to look for something else?")
            continue

        print(f"For {category}, these sizes are available: {', '.join(available_sizes)}")
        size_input = input("You: ").strip()

        if size_input.lower() not in [size.lower() for size in available_sizes]:
            print(f"I'm sorry, but I don't have size '{size_input}' for {category}. 😕")
            print("Would you like to try a different size?")
            continue

        # Get and present color options
        available_colors = get_available_colors_for_category_and_size(category, size_input)
        if not available_colors:
            print(f"Oh no! It seems we're out of {category} items in size {size_input}. 😔")
            print("Would you like to try a different size?")
            continue

        print(f"For {category} in size {size_input}, these colors are available: {', '.join(available_colors)}")
        color_input = input("You: ").strip()

        if color_input.lower() not in [color.lower() for color in available_colors]:
            print(f"I'm sorry, but {color_input} isn't available for this {category} in size {size_input}. 😕")
            print(f"Would you like to choose from our available colors?")
            continue

        # Find and present matching products
        matching_products = find_products_by_criteria(category, size_input, color_input)
        if not matching_products:
            print(f"I couldn't find any {category} in size {size_input} and color {color_input}. 😔")
        else:
            print("Here are some products you might like:")
            for product in matching_products:
                recommendation = generate_product_recommendation(product)
                print(f"- {product['product_name']} by {product['product_company_name']}: {recommendation}")

        print("\nWould you like to look for something else? (yes/no)")
        continue_shopping = input("You: ").strip().lower()
        if continue_shopping != 'yes':
            print("Thanks for shopping with me today! Hope to see you again soon! 👋")
            break

if __name__ == "__main__":
    chat_with_assistant()
