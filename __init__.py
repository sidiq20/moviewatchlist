import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

from routes import pages

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "20bc721c9186545533e0db2372305f40"
    )

    client = MongoClient(app.config["MONGODB_URI"])

    app.db = client.get_database("moviewatchlist")

    app.register_blueprint(pages)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, use_reloader=False, port=7000)