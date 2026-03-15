import os
from functools import wraps

import jwt
from flask import jsonify, request


def token_required(f):
    """
    Decorator that protects a route with JWT auth.

    Usage:
        @app.get("/tasks")
        @token_required
        def get_tasks(current_user):
            # current_user = {"id": 1, "email": "alice@example.com"}
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or malformed token."}), 401

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                os.environ.get("JWT_SECRET", "dev-jwt-secret"),
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token."}), 401

        return f(payload, *args, **kwargs)

    return decorated
