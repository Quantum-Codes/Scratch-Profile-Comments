from flask import Flask, jsonify, redirect, request
from api import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
	return redirect("https://github.com/Quantum-Codes/Profile-comments-API/wiki"), 302

@app.route('/comments/', methods=['GET'])
def return_data():
	username = request.args.get('username', default="%hello@")
	limit = request.args.get('limit', default="all", type=str)
	page = int(request.args.get('page', default=1, type=int))
	d = []
	if username == "%hello@":
		return {"error": "username arguement is mandatory"}, 404
	if limit == "0":
		limit = int(limit)
		try:
			return get_comments(username, page)[limit]
		except KeyError:
			return {"error": "page doesn't exist"}, 404
	elif limit.isnumeric():
		limit = int(limit)
		try:
			done = 0
			p = page
			while done != limit:
				comments = get_comments(username, p)
				for i in range(0, len(comments)):
					try:
						d.append(comments[i])
					except KeyError:
						return {"error": "page doesn't exist"}, 404
					done += 1
					if done == limit: break
				p += 1
			return jsonify(d), 200
		except IndexError:
			return {"Error": "Limit too high!"}, 404
	else:
		return jsonify(get_comments(username, page)), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=105, debug=True)
