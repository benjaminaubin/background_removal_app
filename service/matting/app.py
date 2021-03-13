import numpy as np
from flask import Flask, request, jsonify

from .main import predict_matting
from .networks import build_model


app = Flask(__name__)


@app.route("/", methods=["POST"])
def gen_trimap():
    data = request.get_json()
    image = np.array(data["image"])
    trimap = np.array(data["trimap"])

    device = "cpu"
    try:
        model_matting = build_model(dir_weights="./weights/", weights="FBA.pth", device=device)
        fg, bg, alpha = predict_matting(image, trimap, model_matting, device=device)
        composite = fg * alpha[:, :, None]

        return jsonify(
            {
                "statusCode": 200,
                "status": "Matting success",
                "composite": composite.tolist(),
                "alpha": alpha.tolist(),
                "fg": fg.tolist(),
                "bg": bg.tolist(),
            }
        )

    except:
        return jsonify({"statusCode": 500, "status": "Matting failed", "output": []})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
