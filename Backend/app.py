from flask import Flask, request, jsonify
from flask_cors import CORS
from search_setup import ramayan_search

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

        user_input = data["question"]
        results = ramayan_search.search(user_input, k=1)

        if results:
            # Get the best available translation or meaning
            translation = results[0].get('translation', '')
            meaning = results[0].get('meaning', '')
            
            # Create a natural response
            if translation and meaning:
                response = {
                    "answer": f"{translation}\n\n{meaning}"
                }
            elif translation:
                response = {
                    "answer": translation
                }
            elif meaning:
                response = {
                    "answer": meaning
                }
            else:
                response = {
                    "answer": "Sorry, I couldn't find a clear answer to your question."
                }
            return jsonify(response)
        else:
            return jsonify({"answer": "Sorry, I don't have an answer for that."})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
