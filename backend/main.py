from flask import Flask, jsonify
import asyncio
from backend.dependencies import register_dependencies
from backend.core.fallout_news_logic import run_bunker_sequence

app = Flask(__name__)
container = register_dependencies()

@app.route("/bunker", methods=["GET"])
def bunker_route():
    headlines, response = asyncio.run(run_bunker_sequence(container))
    return jsonify({
        "headlines": headlines,
        "response": response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)