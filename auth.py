import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from flask import Blueprint, jsonify, request

import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email    = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", "")).strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    # Check if email already taken
    existing = db.execute(
        "SELECT id FROM users WHERE email = %s",
        (email,),
        fetchone=True,
    )
    if existing:
        return jsonify({"error": "Email already registered."}), 409

    # Hash the password — bcrypt handles salt automatically
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    db.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s)",
        (email, hashed),
    )

    return jsonify({"message": "Account created. You can now log in."}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email    = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", "")).strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = db.execute(
        "SELECT id, email, password FROM users WHERE email = %s",
        (email,),
        fetchone=True,
    )

    # Same error message for wrong email or wrong password (security best practice)
    if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"error": "Invalid email or password."}), 401

    token = jwt.encode(
        {
            "id":    user["id"],
            "email": user["email"],
            "exp":   datetime.now(timezone.utc) + timedelta(days=7),
        },
        os.environ.get("JWT_SECRET", "dev-jwt-secret"),
        algorithm="HS256",
    )

    return jsonify({"token": token}), 200
