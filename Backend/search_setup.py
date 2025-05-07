import json
import requests
import re
import random

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
    
    def get_random_shloka(self, k=1):
        """Get random shlokas from the dataset with extracted keywords for question generation"""
        if not self.data:
            return []
            
        # Get k random shlokas
        selected_shlokas = []
        for _ in range(k):
            if len(self.data) > 0:
                shloka = random.choice(self.data)
                
                # Extract potential keywords from the translation or meaning
                keywords = []
                text = shloka.get('translation', '') or shloka.get('meaning', '')
                if text:
                    # Get important words (nouns, proper nouns) - simplified approach
                    words = re.findall(r'\b[A-Z][a-z]+\b', text)  # Find proper nouns (capitalized words)
                    if words:
                        keywords = words[:3]  # Take up to 3 keywords
                    else:
                        # If no proper nouns, take some longer words as they might be important
                        all_words = re.findall(r'\b[a-z]{5,}\b', text.lower())
                        keywords = all_words[:3] if all_words else ['wisdom', 'dharma', 'devotion']
                
                selected_shlokas.append({
                    'shloka': shloka.get('shloka', ''),
                    'meaning': shloka.get('meaning', ''),
                    'translation': shloka.get('translation', ''),
                    'explanation': shloka.get('explanation', ''),
                    'keywords': keywords
                })
                
        return selected_shlokas

# Create a global instance
ramayan_search = RamayanSearch()
