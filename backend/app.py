"""Flask application factory.

This module exposes a ``create_app`` function used by ``app.py`` in the project
root.  It initialises the :class:`~flask.Flask` instance, sets up CORS and
registers all HTTP routes.

Routes are currently defined in :mod:`backend.main`, so this factory simply
imports those view functions and attaches them to the new application instance.
"""

from flask import Flask
from flask_cors import CORS

# Import existing route handlers from ``backend.main``.  They rely on a global
# dependency container defined in that module.
from backend import main as main_routes


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns
    -------
    Flask
        Configured Flask app instance.
    """

    app = Flask(__name__)
    CORS(app)

    # Register routes defined in ``backend.main``.
    app.add_url_rule(
        "/bunker", view_func=main_routes.bunker_route, methods=["GET"]
    )
    app.add_url_rule(
        "/bunker/audio", view_func=main_routes.bunker_audio, methods=["GET"]
    )

    return app


