from flask import Flask, render_template, request, jsonify
from model_response import generate_response
app = Flask(__name__)

# Define a basic route
@app.route('/')
def index():
    return render_template('testing.html')

@app.route('/api', methods=['POST'])
def api():
    print(request.get_json())
    data = request.get_json()
    response = generate_response(data['user_input'])
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)