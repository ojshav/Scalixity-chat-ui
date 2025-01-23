from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from FAQ import main as faq_main
from Shopping_assistant import (
    chat_with_assistant, 
    get_available_categories, 
    get_available_sizes_for_category, 
    get_available_colors_for_category_and_size, 
    find_products_by_criteria,
    generate_product_recommendation
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    choice = data.get('choice')
    user_input = data.get('input', '')

    if choice == '1':  # FAQ
        response = faq_main(user_input)
        if "error" in response:
            return jsonify({"content": response["error"]})
        else:
            return jsonify({"content": response["answer"], "processing_time": response["processing_time"]})

    elif choice == '2':  # Shopping Assistant
        if user_input.startswith('get_categories'):
            response = get_available_categories()
        elif user_input.startswith('get_sizes'):
            _, category = user_input.split(' ', 1)
            response = get_available_sizes_for_category(category)
        elif user_input.startswith('get_colors'):
            _, category, size = user_input.split(' ', 2)
            response = get_available_colors_for_category_and_size(category, size)
        elif user_input.startswith('find_products'):
            _, category, size, color = user_input.split(' ', 3)
            products = find_products_by_criteria(category, size, color)
            
            # Generate LLM-based recommendations for each product
            recommended_products = []
            for product in products:
                recommendation = generate_product_recommendation(product)
                recommended_products.append({
                    "name": str(product['product_name']),
                    "company": str(product['product_company_name']),
                    "recommendation": str(recommendation)
                })
            
            response = recommended_products

    else:
        response = {"error": "Invalid choice. Please select a valid option."}

    return jsonify({"content": response})

if __name__ == "__main__":
    app.run(debug=True)