from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
counter = Counter('flask_requests_total', 'Total requests served')

@app.route('/')
def home():
    counter.inc()
    return jsonify({"message": "Welcome to Prometheus-monitored Flask app"})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
