# GestureON - Sign languange recognition

Application for hand gesture recognition in real time with use of MediaPipe, OpenCV and PyQt5.

## Installation
Linux
```bash
git clone <repo>
cd project

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Windows

Download the latest `.exe` from Releases and run it.


## Usage

Select a camera source, then choose one of the modes:

- **Test** – run gesture recognition using the trained model  
- **Collect** – collect training data for the selected gesture  

In Collect mode, you can select the current gesture by its ID (defined in the `GestureLabel` enum in `config.py`).



## Controls
s - save current data position to dataset (.csv) 
c - change selected gesture label  
q - quit application
