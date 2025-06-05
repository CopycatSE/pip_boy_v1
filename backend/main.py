from flask import Flask, jsonify
from flask import send_file
from flask_cors import CORS
import asyncio
from backend.dependencies import register_dependencies
from backend.core.fallout_news_logic import run_bunker_sequence

app = Flask(__name__)
# Allow all origins for development purposes (consider tightening this in production)
CORS(app)

container = register_dependencies()

@app.route("/bunker", methods=["GET"])
def bunker_route():
    headlines, response = asyncio.run(run_bunker_sequence(container))
    return jsonify({
        "headlines": headlines,
        "response": response
    })


# New route for serving audio file
@app.route("/bunker/audio", methods=["GET"])
def bunker_audio():
    try:
        return send_file("output.mp3", mimetype="audio/mpeg")
    except FileNotFoundError:
        return "Audio file not found", 404

import socket


# system configurations

# This block  finds a free port in the specified range (default: 5000-5100) for CORS implementation.
def find_free_port(start=5000, end=5100):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    raise RuntimeError("No free port found in the specified range")

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Flask API for Pip-Boy")
    parser.add_argument("--port", type=int, help="Port number to run the server on (default: first free port starting from 5000)")
    args = parser.parse_args()

    selected_port = args.port if args.port else find_free_port()
    print(f" Starting server on port {selected_port}")
    app.run(host="0.0.0.0", port=selected_port)