from flask import Flask, jsonify, request
from flask_cors import CORS
import word_generator
import re
import random
import csv

app = Flask(__name__)
CORS(app)

used_words = set()  # Keep track of used words

@app.route('/words', methods=['GET'])
def get_words():
    words_examples = [
        'web App', 'mobile App', 'database', 'user Interface',
        'code Example', 'programming Language', 'software Development', 'application Framework',
        'algorithm Design', 'functionality Test', 'variable Declaration', 'class Definition',
        'machine Learning', 'data Science', 'neural Network', 'visualization Technique',
        'cloud Computing', 'backend Development', 'frontend Framework', 'software Framework',
        'authentication Method', 'authorization Process', 'security Protocol', 'encryption Algorithm'
    ]

    # Filter out used words
    available_words = [word for word in words_examples if word not in used_words]

    # If all words have been used, reset the used_words set
    if not available_words:
        used_words.clear()
        available_words = words_examples

    test_word = random.choice(available_words)

    # Add the chosen word to the set of used words
    used_words.add(test_word)

    result_object = {
        'options_camel_case': word_generator.generate_task(test_word),
        'options_kebab_case': word_generator.generate_task(test_word)
    }

    return jsonify(result_object)

answer_data_list = []

# Define the route to handle both submitting and exporting answer data
@app.route('/submit-and-export', methods=['POST', 'GET'])
def submit_and_export():
    if request.method == 'POST':
        # Handle POST request to submit answer data
        answer_data = request.get_json()

        # Append experiment information to the answer data
        experiment_info = f"Experiment {len(answer_data_list) + 1}"
        answer_data_with_info = {**answer_data, 'experiment_info': experiment_info}

        # Append answer data to the in-memory list
        answer_data_list.append(answer_data_with_info)

        return jsonify({"message": "Answer data submitted successfully"})
    
    elif request.method == 'GET':
        # Handle GET request to export answer data to a CSV file

        # Define the CSV file path
        csv_file_path = 'answer_data.csv'

        # Define CSV header
        csv_header = ['experiment_info', 'word', 'clickedWord', 'isCorrect', 'timeTaken']

        # Write answer data to CSV file
        with open(csv_file_path, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_header)

            # Write a newline to separate experiments in the CSV file
            csv_file.write("\n")

            # Write experiment information and answer data to CSV file
            for answer_data in answer_data_list:
                writer.writerow(answer_data)

    # Clear the answer_data_list after exporting to CSV
    answer_data_list.clear()

    return jsonify({"message": f"Answer data exported to {csv_file_path} successfully"})

if __name__ == '__main__':
    app.run(debug=True)