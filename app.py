import datetime
from flask_cors import CORS
from flask import Flask, request, jsonify
import time
x = datetime.datetime.now()
 
# Initializing flask app
app = Flask(__name__)
CORS(app)
 
messages = []
 
# Route for seeing a data
@app.route('/members')
def members():
    return { "members": ["Member1", "Member2", "Member3"] }

@app.route('/send-message', methods=['POST'])
def send_message():
    print('收倒')
    data = request.get_json()
    message = data.get('message')
    messages.append(message)
    # return jsonify({'message': message}), 200
    time.sleep(5)
    return jsonify({'message': f'收到${message}'}), 200 # type: ignore


# Running app
if __name__ == '__main__':
    app.run(debug=True)
