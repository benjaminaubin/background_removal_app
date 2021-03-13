import torch
import torchvision
import torchvision.transforms as T
import numpy as np

class MaskRCNN:
    def __init__(self, confidence_thresh=0.6):
        self.model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
        self.model.eval()
        self.transform = T.Compose([T.ToTensor()])
        self.conf_thresh = confidence_thresh
        

    def get_seg_output(self, image:np.array):
        image = self.transform(image.copy()).type('torch.FloatTensor')
        with torch.no_grad():
            pred = self.model([image])
            
        #outputs = [(pred[0]['masks'][i][0],pred[0]['labels'][i]) for i in range(len(pred[0]['boxes'])) if pred[0]['scores'][i]>self.conf_thresh and pred[0]['labels'][i]==1]
        outputs = [(pred[0]['masks'][i][0], pred[0]['labels'][i]) for i in range(len(pred[0]['boxes'])) if pred[0]['scores'][i]>self.conf_thresh]
        return outputs
     