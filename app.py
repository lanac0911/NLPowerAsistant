# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     # path = './frontend/public/index.html'
#     # path ='frontend/build/index.html'
#     return render_template('index.html') 
#     # return render_template(path) 

# if __name__ == '__main__':
#     app.run('127.0.0.1', port=5000, debug=True)

# Filename - server.py
 
# Import flask and datetime module for showing date and time
from flask import Flask
import datetime
from flask_cors import CORS

x = datetime.datetime.now()
 
# Initializing flask app
app = Flask(__name__)
 
 
# Route for seeing a data
@app.route('/members')
def members():
    return { "members": ["Member1", "Member2", "Member3"] }

 

# Running app
CORS(app)
if __name__ == '__main__':
    app.run(debug=True)