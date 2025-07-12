# HandGesture Recognition

Control slide presentations using hand gestures via your device's camera.

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -r config/requirements.txt

# Run the web interface
python src/main.py

# Or run gesture controller directly
python src/gesture.py
```

## 📁 Project Structure

```
Handgesture-Recognition/
├── 📁 src/                          # Source code
│   ├── main.py                      # Streamlit web app
│   ├── gesture.py                   # Gesture controller
│   ├── theft.py                     # Alternative conversion
│   └── test_gesture.py              # Test script
│
├── 📁 config/                       # Configuration
│   ├── gesture_config.json          # Gesture settings
│   └── requirements.txt             # Dependencies
│
├── 📁 data/                         # Data and assets
│   ├── presentations/               # Original PPTX files
│   ├── slides/                      # Converted images
│   └── samples/                     # Sample images
│
├── 📁 docs/                         # Documentation
│   ├── README.md                    # This file
│   └── reports/                     # Project reports
│
└── 📁 assets/                       # Static assets
    └── logo.png                     # Project logo
```

## 🎯 Features

- **Hand Gesture Recognition**: Control slides with hand movements
- **Real-time Processing**: Live camera feed with gesture detection
- **Annotation Tools**: Draw and annotate on slides
- **Web Interface**: Upload and convert presentations via Streamlit
- **Configurable**: Easy customization via JSON config

## 📖 Usage

### Web Interface
1. Run `python src/main.py`
2. Upload your PPTX file
3. Convert slides to images
4. Start gesture control

### Direct Gesture Control
1. Place images in `data/slides/images/`
2. Run `python src/gesture.py`
3. Use hand gestures to control slides

## 🎮 Gestures

- **👆 Index finger only**: Previous slide / Draw
- **👍 Thumb up**: Next slide
- **🤟 Three fingers**: Erase annotation
- **✌️ Two fingers**: Pointer mode

## 🔧 Configuration

Edit `config/gesture_config.json` to customize:
- Camera resolution
- Gesture sensitivity
- Annotation colors
- Custom gesture patterns

## 📚 Documentation

- [Gesture Controller Guide](docs/README.md)
- [Project Reports](docs/reports/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python src/test_gesture.py`
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Happy presenting! 🎤✨**
