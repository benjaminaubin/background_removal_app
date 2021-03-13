from torch.utils.data import Dataset
import numpy as np
import cv2
import os
import torch


class PredDataset(Dataset):
    """Reads image and trimap pairs from folder."""

    def __init__(self, img_dir, trimap_dir):
        self.img_dir, self.trimap_dir = img_dir, trimap_dir
        self.img_names = [x for x in os.listdir(self.img_dir) if "png" in x]

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, idx):
        img_name = self.img_names[idx]

        image = read_image(os.path.join(self.img_dir, img_name))
        trimap = read_trimap(os.path.join(self.trimap_dir, img_name))
        pred_dict = {"image": image, "trimap": trimap, "name": img_name}

        return pred_dict


def read_image(name):
    img = cv2.imread(name)
    return (img / 255.0)[:, :, ::-1]


def read_trimap(name):
    trimap_im = cv2.imread(name, 0) / 255.0
    h, w = trimap_im.shape
    trimap = np.zeros((h, w, 2))
    trimap[trimap_im == 1, 1] = 1
    trimap[trimap_im == 0, 0] = 1
    return trimap


def np_to_torch(x, device):
    if device == "cuda":
        return torch.from_numpy(x).permute(2, 0, 1)[None, :, :, :].float().cuda()
    elif device == "cpu":
        return torch.from_numpy(x).permute(2, 0, 1)[None, :, :, :].float()
    else:
        raise NotImplementedError


def scale_input(x: np.ndarray, scale: float, scale_type) -> np.ndarray:
    """
    Scales inputs to multiple of 8.
    """
    h, w = x.shape[:2]
    h1 = int(np.ceil(scale * h / 8) * 8)
    w1 = int(np.ceil(scale * w / 8) * 8)
    x_scale = cv2.resize(x, (w1, h1), interpolation=scale_type)
    return x_scale
