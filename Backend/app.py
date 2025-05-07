# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from search_setup import ramayan_search
# import json
# import os
# import re

# app = Flask(__name__)
# CORS(app)

# FAQS_FILE = "Backend/data/faqs.json"

# print("✅ Ramayan Search System initialized.")

# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     try:
#         data = request.get_json()
#         print("Received request:", data)

#         if not data or "question" not in data:
#             return jsonify({"error": "No question provided"}), 400

#         user_input = data["question"]

#         # Check FAQs if available
#         if os.path.exists(FAQS_FILE) and os.path.getsize(FAQS_FILE) > 0:
#             with open(FAQS_FILE, 'r') as f:
#                 faqs = json.load(f)

#             best_match = None
#             highest_score = 0

#             # Handle both list and dict structures
#             if isinstance(faqs, dict):
#                 faq_items = []
#                 for category, questions in faqs.items():
#                     faq_items.extend(questions)
#             elif isinstance(faqs, list):
#                 faq_items = faqs
#             else:
#                 faq_items = []

#             for item in faq_items:
#                 if isinstance(item, dict):  # Make sure each item is a dictionary
#                     faq_question = item.get("question", "").lower()
#                     faq_answer = item.get("answer", "")
#                 else:
#                     faq_question = ""
#                     faq_answer = ""

#                 user_question = user_input.lower()

#                 faq_words = set(re.findall(r'\b[a-z]{3,}\b', faq_question))
#                 user_words = set(re.findall(r'\b[a-z]{3,}\b', user_question))

#                 stopwords = {'what', 'why', 'how', 'when', 'where', 'which', 'who', 'whom', 'whose', 'the', 'and', 'but', 'for', 'that', 'this', 'with', 'from'}
#                 faq_words -= stopwords
#                 user_words -= stopwords

#                 if not user_words:
#                     continue

#                 common_words = faq_words.intersection(user_words)
#                 score = len(common_words) / len(user_words)

#                 # Boost score if key terms are present
#                 key_terms = ['hanuman', 'sita', 'rama', 'lanka', 'ravana']
#                 for term in key_terms:
#                     if term in faq_question and term in user_question:
#                         score += 0.3

#                 if score > highest_score and score > 0.4:
#                     highest_score = score
#                     best_match = item

#             if best_match:
#                 return jsonify({"answer": best_match["answer"]})

#         # If no FAQ match, fallback to Ramayan search
#         results = ramayan_search.search(user_input, k=1)

#         if results:
#             translation = results[0].get('translation', '')
#             meaning = results[0].get('meaning', '')
#             explanation = results[0].get('explanation', '')

#             if translation and explanation:
#                 response = f"{translation}\n\n{explanation}"
#             elif translation and meaning:
#                 response = f"{translation}\n\n{meaning}"
#             elif translation:
#                 response = translation
#             elif meaning:
#                 response = meaning
#             else:
#                 response = "Sorry, I couldn't find a clear answer to your question."

#             return jsonify({"answer": response})
#         else:
#             return jsonify({"answer": "Sorry, I don't have an answer for that."})

#     except Exception as e:
#         print("❌ Error:", str(e))
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)


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

        # Check FAQs if available
        if os.path.exists(FAQS_FILE) and os.path.getsize(FAQS_FILE) > 0:
            with open(FAQS_FILE, 'r') as f:
                faqs = json.load(f)

            best_match = None
            highest_score = 0

            # Handle both list and dict structures
            if isinstance(faqs, dict):
                faq_items = []
                for category, questions in faqs.items():
                    faq_items.extend(questions)
            elif isinstance(faqs, list):
                faq_items = faqs
            else:
                faq_items = []

            for item in faq_items:
                if isinstance(item, dict):  # Make sure each item is a dictionary
                    faq_question = item.get("question", "").lower()
                    faq_answer = item.get("answer", "")
                else:
                    faq_question = ""
                    faq_answer = ""

                user_question = user_input.lower()

                faq_words = set(re.findall(r'\b[a-z]{3,}\b', faq_question))
                user_words = set(re.findall(r'\b[a-z]{3,}\b', user_question))

                stopwords = {'what', 'why', 'how', 'when', 'where', 'which', 'who', 'whom', 'whose', 'the', 'and', 'but', 'for', 'that', 'this', 'with', 'from'}
                faq_words -= stopwords
                user_words -= stopwords

                if not user_words:
                    continue

                common_words = faq_words.intersection(user_words)
                score = len(common_words) / len(user_words)

                # Boost score if key terms are present
                key_terms = ['hanuman', 'sita', 'rama', 'lanka', 'ravana']
                for term in key_terms:
                    if term in faq_question and term in user_question:
                        score += 0.3

                if score > highest_score and score > 0.4:
                    highest_score = score
                    best_match = item

            if best_match:
                return jsonify({"answer": best_match["answer"]})

        # If no FAQ match, fallback to Ramayan search
        results = ramayan_search.search(user_input, k=1)

        if results:
            explanation = results[0].get('explanation', '')

            if explanation:
                response = explanation
            else:
                response = "Sorry, I couldn't find a clear explanation for your question."

            return jsonify({"answer": response})
        else:
            return jsonify({"answer": "Sorry, I don't have an answer for that."})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
