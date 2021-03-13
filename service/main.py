import cv2
import numpy as np
import argparse
import requests
import matplotlib.pyplot as plt
import os
from trimap.utils import read_image


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str,
                        default="./examples/images/4.jpeg")
    args = parser.parse_args()

    ## Load image ##
    assert os.path.exists(args.path)
    image = read_image(args.path)

    ## Generates trimap ##
    response_trimap = requests.post(
        "http://127.0.0.1:3001/", json={"input": image.tolist()})
    trimap = np.array(response_trimap.json()["output"])

    ## Generates matting ##
    response_matting = requests.post(
        "http://127.0.0.1:3002/", json={"image": image.tolist(), "trimap": trimap.tolist()}
    )
    composite = np.array(response_matting.json()["composite"])
    alpha = np.array(response_matting.json()["alpha"])

    ## Plot ##
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs = axs.flatten()
    axs[0].set_title("Original")
    axs[0].imshow(image)
    axs[1].set_title("Alpha Matte")
    axs[1].imshow(alpha, cmap="gray", vmin=0, vmax=1)
    axs[2].set_title("Composite")
    axs[2].imshow(composite)

    plt.show(block=False)
    input()
    plt.close()
