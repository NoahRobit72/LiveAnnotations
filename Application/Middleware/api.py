from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

# Initial coordinates

# @app.route('/')
# def index():
#     return render_template('index.html', coordinates=coordinates)

@app.route('/update_coordinates')
def update_coordinates():
    coordinates = {"top": "100", "left": "100"}

    return jsonify(coordinates)

if __name__ == '__main__':
    app.run(debug=True, port=8080)