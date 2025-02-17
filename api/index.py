from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Flask Proxy Server!"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    target_url = f"http://example.com/{path}"
    method = request.method
    data = request.get_data()
    headers = {key: value for key, value in request.headers if key != 'Host'}
    response = requests.request(method, target_url, headers=headers, data=data)
    proxy_response = Response(response.content, status=response.status_code)
    for header in response.headers:
        proxy_response.headers[header] = response.headers[header]
    return proxy_response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
