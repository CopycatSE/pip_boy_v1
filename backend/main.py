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

# This block sets the CORS port to a fixed value (5000).
def find_free_port(start=5000, end=5100):
    # Always return 5000 for CORS usage
    return 5000

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Flask API for Pip-Boy")
    parser.add_argument("--port", type=int, help="Port number to run the server on (default: 5000)")
    args = parser.parse_args()

    selected_port = args.port if args.port else 5000
    print(f" Starting server on port {selected_port}")
    app.run(host="0.0.0.0", port=selected_port)