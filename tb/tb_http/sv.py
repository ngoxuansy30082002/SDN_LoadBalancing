from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/demo", methods=["POST"])
def server():
    if request.content_type == 'application/x-www-form-urlencoded':
        req = request.form.to_dict()
    elif request.content_type == 'application/json':
        req = request.get_json()
    else:
        return jsonify({'status': 1, 'msg': 'unsupported content type'})

    # print(f"user req: {req}")
    w = int(req.get("width", 0))
    h = int(req.get("height", 0))

    return jsonify({'status': 0, 'msg': "ok", "area": w*h})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
