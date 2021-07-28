from flask import Flask, jsonify
import json
from flask import request
from api import *
import test

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    message = {
        "Message": "Welcome To Scratch User Comments API",
        "Developers": "Ankit Anmol and Siddhesh Chavan",
        "Documentation": "A link : https://scratch-profile-comments.sid72020123.repl.co/user/?username=Ankit_Anmol&limit=100"
    }
    return f"{json.dumps(message)}", 200


@app.route('/user/', methods=['GET'])
def return_data():
    username = request.args.get('username')
    limit = int(request.args.get('limit', default=0, type=int))
    page = int(request.args.get('page', default=1, type=int))
    d = []
    if limit == 0:
      return get_comments(username, page)[limit]
    if limit > 0:
      try:
        comments = get_comments(username, page)
        for i in range(0, limit):
            d.append(comments[i])
        return jsonify(d), 200
      except IndexError:
        message = {
          "Error": "Limit too high!"
        }
        return f"{json.dumps(message)}", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)
