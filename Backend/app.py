from flask import Flask, request, jsonify
from flask_cors import CORS
from search_setup import ramayan_search
import json
import os
import re

app = Flask(__name__)
CORS(app)

FAQS_FILE = "Backend/data/faqs.json"

print("✅ Ramayan Search System initialized.")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        print("Received request:", data)

        if not data or "question" not in data:
            return jsonify({"error": "No question provided"}), 400

        user_input = data["question"]
        
        # First check if there's a match in our FAQs
        if os.path.exists(FAQS_FILE) and os.path.getsize(FAQS_FILE) > 0:
            with open(FAQS_FILE, 'r') as f:
                faqs = json.load(f)
            
            best_match = None
            highest_score = 0
            
            # Search for related questions in FAQs using more sophisticated matching
            for category, questions in faqs.items():
                for item in questions:
                    # Calculate similarity score based on word overlap
                    faq_question = item["question"].lower()
                    user_question = user_input.lower()
                    
                    # Extract words (removing common stopwords)
                    faq_words = set(re.findall(r'\b[a-z]{3,}\b', faq_question))
                    user_words = set(re.findall(r'\b[a-z]{3,}\b', user_question))
                    
                    # Ignore common words that don't help with matching
                    stopwords = {'what', 'why', 'how', 'when', 'where', 'which', 'who', 'whom', 'whose', 'the', 'and', 'but', 'for', 'that', 'this', 'with', 'from'}
                    faq_words = faq_words - stopwords
                    user_words = user_words - stopwords
                    
                    if not user_words:  # If all user words were stopwords
                        continue
                    
                    # Calculate word overlap score
                    common_words = faq_words.intersection(user_words)
                    score = len(common_words) / len(user_words) if user_words else 0
                    
                    # Check for key terms specific to this shloka
                    key_terms = []
                    if 'Hanuman' in faq_question and 'Hanuman' in user_question:
                        score += 0.3
                    if 'Sita' in faq_question and 'Sita' in user_question:
                        score += 0.3
                    if 'Rama' in faq_question and 'Rama' in user_question:
                        score += 0.3
                    if 'Lanka' in faq_question and 'Lanka' in user_question:
                        score += 0.3
                    if 'Ravana' in faq_question and 'Ravana' in user_question:
                        score += 0.3
                    
                    # If good enough match found
                    if score > highest_score and score > 0.4:  # Threshold for considering it a match
                        highest_score = score
                        best_match = item
            
            if best_match:
                return jsonify({"answer": best_match["answer"]})
        
        # If no FAQ match, use the original search
        results = ramayan_search.search(user_input, k=1)

        if results:
            # Get the best available translation or meaning
            translation = results[0].get('translation', '')
            meaning = results[0].get('meaning', '')
            explanation = results[0].get('explanation', '')
            
            # Create a natural response
            if translation and explanation:
                response = {
                    "answer": f"{translation}\n\n{explanation}"
                }
            elif translation and meaning:
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
