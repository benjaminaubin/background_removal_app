# Trimap generation

## Setup requirements

```:bash
conda create -n trimap python=3.9
conda activate trimap
python3.9 -m pip install -r requirements.txt
```

## Runing the service

```:bash
FLASK_APP=app.py flask run -p 3001
```

## Removing env

```:bash
conda deactivate
conda remove -n trimap --all
```
