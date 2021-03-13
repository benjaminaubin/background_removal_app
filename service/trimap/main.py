import numpy as np
import cv2
import os

from .utils import read_image, Preprocessing
from .models import MaskRCNN


def predict_trimap(image, model):
    """
    Predict trimap with from a segmentation model
    """

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    preprocessor = Preprocessing(kernel)

    image = np.array(image)
    output = model.get_seg_output(image)
    masks = np.array([mask.cpu().numpy() for mask, classes in output])

    if len(masks) == 0:
        raise NameError("Segmentation failed")

    trimap = preprocessor.get_trimap(masks)

    return trimap


if __name__ == "__main__":

    path = "../examples/images/4.jpeg"
    assert os.path.exists(path)
    image = read_image(path)

    ## Generate trimap ##
    model = MaskRCNN(confidence_thresh=0.6)
    trimap = predict_trimap(image, model)
