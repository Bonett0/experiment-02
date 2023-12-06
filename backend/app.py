from flask import Flask, jsonify, request
from flask_cors import CORS
import word_generator
import re
import random
import csv

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

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

    test_word = random.choice(words_examples)

    result_object = {
        'options_camel_case': word_generator.generate_task(test_word),
        'options_kebab_case': word_generator.generate_task(test_word)
    }

    return jsonify(result_object)

answer_data = []

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.get_json()

    # Add the received answer data to the answer_data list
    answer_data.append(data)

    return jsonify({'message': 'Answer received successfully'})

@app.route('/write-to-csv', methods=['GET'])
def write_to_csv():
    # Write the answer_data to a CSV file
    with open('answers.csv', 'w', newline='') as csvfile:
        fieldnames = ['word', 'clickedWord', 'isCorrect', 'timeTaken']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(answer_data)

    return jsonify({'message': 'CSV file written successfully'})

if __name__ == '__main__':
    app.run(debug=True)