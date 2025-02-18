from flask import Flask, request, Response, send_from_directory, jsonify
import requests
import os
from bs4 import BeautifulSoup
import logging

app = Flask(__name__, static_folder='../static')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Construct the target URL
    target_url = f"https://{path}"
    logging.info(f"Proxying request to: {target_url}")
    
    # Fetch the method and data from the original request
    method = request.method
    data = request.get_data()
    headers = {key: value for key, value in request.headers if key != 'Host'}
    
    # Make the request to the target server
    try:
        response = requests.request(method, target_url, headers=headers, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to {target_url} failed: {e}")
        return jsonify({'error': str(e)}), 500

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'
    body_text = soup.get_text()

    # Log the parsed information
    logging.info(f"Title: {title}")
    logging.info(f"Content length: {len(body_text)} characters")

    # Create a JSON response
    proxy_response = jsonify({
        'title': title,
        'content': body_text[:1000]  # Limit content to 1000 characters
    })

    return proxy_response

if __name__ == '__main__':
    app.run()
