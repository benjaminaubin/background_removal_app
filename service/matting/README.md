# Matting

## Setup requirements

```:bash
conda create -n matting python=3.9
conda activate matting
python3.9 -m pip install -r requirements.txt
```

## Runing the service

```:bash
FLASK_APP=app.py flask run -p 3000
```

## Removing env

```:bash
conda deactivate
conda remove -n matting --all
```
