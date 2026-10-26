# AI Virtual Mouse

Control your computer's mouse pointer using hand gestures captured by your webcam.

## Features

- Detects one hand using MediaPipe Hands.
- Moves the mouse pointer using the index fingertip.
- Performs a left click when the index fingertip and thumb tip come close together.
- Displays the webcam feed and gesture status.

## Requirements

- Python version supported by the installed MediaPipe release.
- A webcam.
- macOS, Windows, or Linux (permissions and behavior may vary by operating system).

## Setup on macOS

Open Terminal and navigate to this project folder:

```bash
cd ~/Desktop/AI-Virtual-Mouse
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If installation fails on Python 3.14, install a Python version supported by the current MediaPipe wheel (for example Python 3.12), then recreate the virtual environment with that version.

## Run

```bash
python app.py
```

- Move your index finger to move the pointer.
- Pinch your index finger and thumb together to click.
- Press `q` while the camera window is active to quit.

## macOS permissions

If the camera does not open, allow Terminal or your Python application to use the camera in **System Settings → Privacy & Security → Camera**.

If pointer movement or clicking is blocked, enable the relevant app under **System Settings → Privacy & Security → Accessibility**. Only grant permissions to applications you trust.

## Troubleshooting

- **Camera unavailable:** close other apps using the camera and check camera permissions.
- **ModuleNotFoundError:** activate `.venv` and run `python -m pip install -r requirements.txt`.
- **Installation fails:** check MediaPipe's supported Python versions for your platform and use a compatible Python version.

## Project structure

```text
AI-Virtual-Mouse/
├── app.py
├── requirements.txt
└── README.md
```
