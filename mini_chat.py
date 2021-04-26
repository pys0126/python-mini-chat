from flask import Flask, jsonify, request, abort, url_for
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resource=r"/*")
message = []

@app.route("/msgs",methods=["GET"])
def msgs():
    return jsonify(message=message,code=200)

@app.route("/send_msg",methods=["POST"])
def send_msg():
    data = request.get_json()
    try:
        data["id"] = message[-1]["id"]+1
        message.append(data)
    except:
        data["id"] = 1
        message.append(data)
    re = requests.put(f"http://0.0.0.0/update/{data['id']}")
    return jsonify(message=message[-1],code=re.status_code)

@app.route("/update/<int:id>",methods=["PUT"])
def update(id):
    for msg in message:
        if msg["id"] == id:
            msg["msg"] == request.get_json("msg")["msg"]
        return jsonify(message=message)
    abort(400)

@app.route("/del",methods=["delete"])
def delete():
    message.pop()
    return jsonify(message=message)

if __name__ == "__main__":
    app.run(debug=True, port=80,host="0.0.0.0")