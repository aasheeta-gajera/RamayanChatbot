import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RamayanSearch:
    def __init__(self, ramayan_file="Backend/data/ramayan.json"):
        self.ramayan_file = ramayan_file
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.passages = []
        self.explanations = []
        self.index = None
        self._load_and_build_index()

    def _load_and_build_index(self):
        if not os.path.exists(self.ramayan_file):
            print(f"⚠ Ramayan file {self.ramayan_file} not found.")
            return

        with open(self.ramayan_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Iterate through sections in the Ramayan file
        for section, shlokas in data.items():
            if isinstance(shlokas, dict):  # Each section can have a dict of shlokas
                for shloka, items in shlokas.items():
                    if isinstance(items, list):  # List of question-answer pairs
                        for item in items:
                            if isinstance(item, dict):
                                passage = item.get("question", "").strip()
                                explanation = item.get("answer", "").strip()
                                if passage and explanation:
                                    self.passages.append(passage)
                                    self.explanations.append(explanation)
                            else:
                                print(f"⚠ Skipped non-dictionary item in section '{section} - {shloka}': {item}")
                    else:
                        print(f"⚠ Section '{section} - {shloka}' is not a list, skipping.")
            else:
                print(f"⚠ Section '{section}' is not a dictionary, skipping.")

        if self.passages:
            embeddings = self.model.encode(self.passages, convert_to_numpy=True, show_progress_bar=True)
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings)
            print(f"✅ Loaded and indexed {len(self.passages)} Ramayan passages.")
        else:
            print("⚠ No Ramayan passages found to index.")

    def search(self, query, k=1, threshold=0.5):
        if not self.index or not self.passages:
            return []

        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            score = 1 / (1 + dist)
            if score >= threshold:
                results.append({
                    'score': score,
                    'passage': self.passages[idx],
                    'explanation': self.explanations[idx]
                })
        return results


# Global instance for app.py to import
ramayan_search = RamayanSearch()
