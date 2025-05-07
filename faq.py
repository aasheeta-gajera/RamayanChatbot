import json

def generate_qa_from_shlokas(input_file, output_file):
    # Load input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        ramayan_data = json.load(f)

    qa_pairs = []

    for entry in ramayan_data:
        kanda = entry.get('kanda', 'Unknown Kanda')
        sarga = entry.get('sarga', 'Unknown Sarga')
        shloka_num = entry.get('shloka', 'Unknown Shloka')

        # Safely handle None values
        explanation = entry.get('explanation') or ''
        translation = entry.get('translation') or ''

        explanation = explanation.strip()
        translation = translation.strip()

        if explanation:
            question = f"What is explained in Shloka {shloka_num} of {kanda}, Sarga {sarga}?"
            answer = explanation
        elif translation:
            question = f"What is the meaning of Shloka {shloka_num} in {kanda}, Sarga {sarga}?"
            answer = translation
        else:
            continue  # Skip if no useful text

        qa_pairs.append({
            "question": question,
            "answer": answer
        })

    # Save output to JSON file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(qa_pairs, f_out, ensure_ascii=False, indent=2)

    print(f"✅ Generated {len(qa_pairs)} question-answer pairs and saved to {output_file}")

# Example usage
generate_qa_from_shlokas('RamayanApi.json', 'ramayan_qa.json')



