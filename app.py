from flask import Flask, jsonify, request, render_template

from backend.rag import ask_question


# --------------------------------------------------
# Flask Application
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "API is healthy"
    })


# --------------------------------------------------
# Chat API
# --------------------------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        # Get JSON data from frontend
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body is empty."
            }), 400

        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "status": "error",
                "message": "Question cannot be empty."
            }), 400

        # Send question to our backend pipeline
        result = ask_question(question)

        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# --------------------------------------------------
# Run Flask Application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )