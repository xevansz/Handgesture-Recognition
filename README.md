# HandGesture Recognition

Control slide presentations using hand gestures via your device's camera.  
This project enables seamless, touchless navigation of presentations using computer vision and gesture recognition.

---

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements and Dependencies](#requirements-and-dependencies)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Description

**HandGesture Recognition** is a Python-based tool that allows you to control PowerPoint presentations using hand gestures detected via your webcam.  
Key features:
- Upload and convert PPTX files to images for gesture-based navigation
- Real-time hand gesture recognition using MediaPipe and CVZone
- Streamlit web interface for easy use
- Customizable gesture mappings and settings

---

## Installation

### 1. Python Version

- **Python 3.8+** is recommended (tested on Python 3.11).

> **Note:**  
> For best results, use on a Linux system with all system dependencies installed.
> It has not been tested on **Windows or mac**.

### 2. Virtual Environment (Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r config/requirements.txt
```

### 4. System Requirements

- **LibreOffice** (for PPTX to PDF conversion)
- **Poppler** (for PDF to image conversion)
  - On Arch Linux: `sudo pacman -S poppler`
  - On Ubuntu: `sudo apt-get install poppler-utils`
- **Webcam** (for gesture recognition)

---

## Usage

### 1. Start the Web Interface

```bash
streamlit run main.py
```

### 2. Upload and Convert a Presentation

- Upload your `.pptx` file via the web interface.
- Click "Convert Slides" to process the presentation.

### 3. Start/Stop Gesture Control

- Click "Start Gesture Control" to begin controlling slides with gestures.
- Click "Stop Presenting" to end the gesture session and release the camera.

### 4. Clean Up

- Use the "Clean Up Files" button to remove generated images and optionally the uploaded PPTX/PDF.

---

## Requirements and Dependencies

### System Dependencies

- LibreOffice (for PPTX to PDF conversion)
- Poppler (for PDF to image conversion)

### Python Dependencies

Defined in **config/requirements.txt** file:
- streamlit >= 1.28.0
- opencv-python >= 4.8.0
- cvzone >= 1.6.0
- mediapipe >= 0.10.0
- numpy >= 1.24.0
- Pillow >= 10.0.0
- pdf2image >= 1.16.3
- python-pptx >= 0.6.21

Install all with:

```bash
pip install -r config/requirements.txt
```

---

## Project Structure

```
Handgesture-Recognition/
├── src/                    # Source code
│   └── gesture.py          # Gesture controller logic
├── main.py                 # Streamlit web app
├── config/                 # Configuration files
│   ├── gesture_config.json # Gesture and app settings
│   └── requirements.txt    # Python dependencies
├── data/                   # Data and assets
│   ├── pptx/               # Uploaded PPTX files
│   ├── slides/             # Converted slides
│   │   ├── images/         # Slide images (PNG/JPG)
│   │   └── pdf/            # Slide PDFs
├── docs/                   # Documentation and reports
│   └── reports/            # Project reports (PDFs)
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## Configuration

All configuration is managed via `config/gesture_config.json`.  
Key options:

```json
{
  "width": 1280,
  "height": 720,
  "gesture_threshold": 600,
  "folder_path": "data/slides/images",
  "detection_confidence": 0.8,
  "max_hands": 1,
  "delay": 7,
  "annotation_color": [0, 0, 255],
  "annotation_thickness": 12,
  "gestures": {
    "next_slide": [0, 0, 0, 0, 1],
    "previous_slide": [1, 0, 0, 0, 0],
    "draw": [0, 1, 0, 0, 0],
    "erase": [0, 1, 1, 1, 0],
    "pointer": [0, 1, 1, 0, 0]
  }
}
```

- **Edit this file** to customize gesture mappings, camera settings, and annotation options.

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the repository** and create a new branch.
2. **Set up your development environment** (see Installation)
3. **Test your changes**
4. **Submit a pull request** with a clear description

---

## License

This project is licensed under the [MIT License](LICENSE).

---

**Happy Presenting! 🎤✨**
