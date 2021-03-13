# Service for background removal

- [trimap service](trimap/README.md) that generates a coarse alpha layer
- [matting service](matting/README.md) that uses the trimap to produce a precise matting image:
  based on [F, B, Alpha Matting](https://github.com/MarcoForte/FBA_Matting):

```:bash
@article{forte2020fbamatting,
  title   = {F, B, Alpha Matting},
  author  = {Marco Forte and François Pitié},
  journal = {CoRR},
  volume  = {abs/2003.07711},
  year    = {2020},
}
```

## Requirements

```:bash
conda create -n bg_removal_service python=3.9
conda activate bg_removal_service
python3.9 -m pip install -r requirements.txt
```
