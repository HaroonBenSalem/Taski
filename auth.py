import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from flask import Blueprint, jsonify, request

import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    """
    Register a new user account.
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "haroon@example.com"
            password:
              type: string
              description: "Minimum 8 characters."
              example: "securepassword123"
    responses:
      201:
        description: Account created successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Account created. You can now log in."
      400:
        description: Missing fields or password too short.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Password must be at least 8 characters."
      409:
        description: Email already registered.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Email already registered."
    """
    data = request.get_json(silent=True) or {}
    email    = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", "")).strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    existing = db.execute(
        "SELECT id FROM users WHERE email = %s",
        (email,),
        fetchone=True,
    )
    if existing:
        return jsonify({"error": "Email already registered."}), 409

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    db.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s)",
        (email, hashed),
    )

    return jsonify({"message": "Account created. You can now log in."}), 201


@auth_bp.post("/login")
def login():
    """
    Login and receive a JWT token.
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "haroon@example.com"
            password:
              type: string
              example: "securepassword123"
    responses:
      200:
        description: Login successful. Returns a JWT token valid for 7 days.
        schema:
          type: object
          properties:
            token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      400:
        description: Missing email or password.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Email and password are required."
      401:
        description: Invalid email or password.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid email or password."
    """
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