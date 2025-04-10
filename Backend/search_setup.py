import json
import requests
import re

class RamayanSearch:
    def __init__(self):
        self.data = self._load_data()
        print("✅ Ramayan data loaded successfully!")

    def _load_data(self):
        url = "https://raw.githubusercontent.com/AshuVj/Valmiki_Ramayan_Dataset/refs/heads/main/data/Valmiki_Ramayan_Shlokas.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data:", response.status_code)
            return []

    def search(self, query, k=1):
        if not self.data:
            return []

        # Simple text matching
        results = []
        for shloka in self.data:
            score = 0
            text_to_search = ""
            
            # Combine all text fields
            if 'shloka' in shloka and shloka['shloka']:
                text_to_search += str(shloka['shloka']) + " "
            if 'meaning' in shloka and shloka['meaning']:
                text_to_search += str(shloka['meaning']) + " "
            if 'translation' in shloka and shloka['translation']:
                text_to_search += str(shloka['translation']) + " "
            if 'explanation' in shloka and shloka['explanation']:
                text_to_search += str(shloka['explanation']) + " "

            # Count matching words
            query_words = set(re.findall(r'\w+', query.lower()))
            text_words = set(re.findall(r'\w+', text_to_search.lower()))
            matching_words = query_words.intersection(text_words)
            score = len(matching_words) / len(query_words) if query_words else 0

            if score > 0:
                results.append({
                    'score': score,
                    'shloka': shloka.get('shloka', ''),
                    'meaning': shloka.get('meaning', ''),
                    'translation': shloka.get('translation', ''),
                    'explanation': shloka.get('explanation', '')
                })

        # Sort by score and get top k results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:k]

# Create a global instance
ramayan_search = RamayanSearch() 