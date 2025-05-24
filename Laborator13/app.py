from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, decode_token
from flask_jwt_extended.exceptions import JWTDecodeError

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "pqwerxnAQF8130"
app.config["JWT_ALGORITHM"] = "HS256"

jwt = JWTManager(app)

users = {
    "user1": {"password": "parola1", "role": "admin"},
    "user2": {"password": "parola2", "role": "owner"},
    "user3": {"password": "parolaX", "role": "owner"}
}

tokens = set()

@app.route('/auth', methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = users.get(username, None)
    if user and user["password"] == password:
        access_token = create_access_token(identity=username, additional_claims={"role": user["role"]})
        tokens.add(access_token)
        print(tokens)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/auth/jwtStore', methods=["GET"])
def verify_jwt():
    header = request.headers.get("Authorization", None)

    if not header:
        return jsonify({"message": "Missing or invalid Authorization header"}), 400

    token = header.replace("Bearer ", "").strip()

    if token not in tokens:
        return jsonify({"message": "Token not found"}), 404
    try:
        decoded = decode_token(token)
        role = decoded.get("role", "guest")
        return jsonify({"role": role}), 200
    except JWTDecodeError:
        return jsonify({"message": "Invalid token"}), 401


@app.route('/auth/jwtStore', methods=["DELETE"])
def logout():
    header = request.headers.get("Authorization", None)
    if not header:
        return jsonify({"message": "Missing or invalid Authorization header"}), 400

    token = header.replace("Bearer ", "").strip()

    if token not in tokens:
        return jsonify({"message": "Token not found"}), 404

    try:
        decode_token(token)
    except JWTDecodeError:
        return jsonify({"message": "Invalid token"}), 401

    tokens.remove(token)
    return jsonify({"message": "Logout successful"}), 200


if __name__ == '__main__':
    app.run()
