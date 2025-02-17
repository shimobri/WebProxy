from flask import Flask, request, Response, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='../static')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Construct the target URL
    target_url = f"http://example.com/{path}"
    
    # Fetch the method and data from the original request
    method = request.method
    data = request.get_data()
    headers = {key: value for key, value in request.headers if key != 'Host'}

    # Make the request to the target server
    response = requests.request(method, target_url, headers=headers, data=data)

    # Create a response object
    proxy_response = Response(response.content, status=response.status_code)
    for header in response.headers:
        proxy_response.headers[header] = response.headers[header]

    return proxy_response

if __name__ == '__main__':
    app.run()
