from flask import Flask, request, jsonify
from flask_cors import CORS
from search_setup import ramayan_search  # Only import ramayan_search now

app = Flask(__name__)
CORS(app)

print("✅ Ramayan Search System initialized.")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        print("Received request:", data)

        if not data or "question" not in data:
            return jsonify({"error": "No question provided"}), 400

        user_input = data["question"].strip()

        # Fallback: search Ramayan
        ramayan_results = ramayan_search.search(user_input, k=1, threshold=0.5)
        if ramayan_results:
            explanation = ramayan_results[0].get('explanation', 'Sorry, I couldn\'t find a clear explanation.')
            return jsonify({"answer": explanation})

        return jsonify({"answer": "Sorry, I don't have an answer for that."})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
