import numpy as np
from flask import Flask, request, jsonify

from .models import MaskRCNN
from .main import predict_trimap

app = Flask(__name__)


@app.route("/", methods=["POST"])
def gen_trimap():
    data = request.get_json()
    image = np.array(data["input"])

    try:
        model = MaskRCNN(confidence_thresh=0.6)
        trimap = predict_trimap(image, model)
        assert len(trimap) > 0

        return jsonify({"statusCode": 200, "status": "Trimap success", "output": trimap.tolist()})

    except:
        return jsonify({"statusCode": 500, "status": "Trimap failed", "output": []})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
