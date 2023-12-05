from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/buttons', methods=['GET'])
def get_buttons():
    buttons = [
        {"id": 1, "label": "Button 1"},
        {"id": 2, "label": "Button 2"},
        # Add more buttons as needed
    ]
    return jsonify(buttons)

if __name__ == '__main__':
    app.run(debug=True)