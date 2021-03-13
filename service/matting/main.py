from torch._C import device
import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt

from .utils import scale_input, np_to_torch, read_image, read_trimap
from .networks import trimap_transform, groupnorm_normalise_image
from .networks import build_model


def predict_matting(image_np: np.ndarray, trimap_np: np.ndarray, model, device: str) -> np.ndarray:
    """Predict alpha, foreground and background.
    Parameters:
    image_np -- the image in rgb format between 0 and 1. Dimensions: (h, w, 3)
    trimap_np -- two channel trimap, first background then foreground. Dimensions: (h, w, 2)
    Returns:
    fg: foreground image in rgb format between 0 and 1. Dimensions: (h, w, 3)
    bg: background image in rgb format between 0 and 1. Dimensions: (h, w, 3)
    alpha: alpha matte image between 0 and 1. Dimensions: (h, w)
    """
    h, w = trimap_np.shape[:2]

    image_scale_np = scale_input(image_np, 1.0, cv2.INTER_LANCZOS4)
    trimap_scale_np = scale_input(trimap_np, 1.0, cv2.INTER_LANCZOS4)

    with torch.no_grad():

        image_torch = np_to_torch(image_scale_np, device)
        trimap_torch = np_to_torch(trimap_scale_np, device)

        trimap_transformed_torch = np_to_torch(trimap_transform(trimap_scale_np), device)
        image_transformed_torch = groupnorm_normalise_image(image_torch.clone(), format="nchw")

        output = model(image_torch, trimap_torch, image_transformed_torch, trimap_transformed_torch)

        output = cv2.resize(output[0].cpu().numpy().transpose((1, 2, 0)), (w, h), cv2.INTER_LANCZOS4)
    alpha = output[:, :, 0]
    fg = output[:, :, 1:4]
    bg = output[:, :, 4:7]

    alpha[trimap_np[:, :, 0] == 1] = 0
    alpha[trimap_np[:, :, 1] == 1] = 1
    fg[alpha == 1] = image_np[alpha == 1]
    bg[alpha == 0] = image_np[alpha == 0]
    return fg, bg, alpha


if __name__ == "__main__":
    device = "cpu"
    path_image = "../examples/images/troll.png"
    path_trimap = "../examples/trimaps/troll.png"

    image = read_image(path_image)
    trimap = read_trimap(path_trimap)

    model_matting = build_model(dir_weights="./weights/", weights="FBA.pth", device=device)
    fg, bg, alpha = predict_matting(image, trimap, model_matting, device=device)

    ## Plot ##
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs = axs.flatten()
    axs[0].set_title("Original")
    axs[0].imshow(image)
    axs[1].set_title("Alpha Matte")
    axs[1].imshow(alpha, cmap="gray", vmin=0, vmax=1)
    axs[2].set_title("Composite")
    axs[2].imshow(fg * alpha[:, :, None])

    plt.show(block=False)
    input()
    plt.close()
