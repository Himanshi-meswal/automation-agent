from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import cohere
import logging

# Load environment variables
load_dotenv(dotenv_path=".../src/.env")
app = Flask(__name__)

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perform_task', methods=['POST'])
def perform_task():
    task = request.form['task']
    if not COHERE_API_KEY:
        return "Cohere API key not found", 500
    try:
        response = co.chat(message=task)
        result = response.text.strip() 
        return {"result": result}, 200
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
