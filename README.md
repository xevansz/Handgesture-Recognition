<h1 align="center">
  HandGesture Recognition
  <img src="https://github.com/xevansz/Handgesture-Recognition/blob/main/logo.png" width="40" height="40" alt="GesturePresenter Logo"/>
</h1>

**Control Slides with just hand gestures!**

HandGesture recognition enables users to control slide presentations through hand gestures, utilizing any device with a camera. This project leverages Google's MediaPipe Hands for gesture recognition.

## Key Components 
- **CVzone** : Developed with ReactJS, this website uses your device's camera to recognize hand gestures for slide control. 
- **numpy** : Facilitates navigation through a Google Slides presentation by communicating with the Remote Website via WebSockets. 

## Screenshots
<table>
  <tr>
    <td><img src="https://lh3.googleusercontent.com/o8aGS4zceshid4rtJhn4aU5qhKl5S4hkjMqN2HtFyYTzEXFmCAbAZcXKm0BjU16CAQiqUkE_uIO52Q2s5xQOenKEqQ=s1600-w1600-h1000" alt="Extension Screenshot" style="width: 100%; max-width: 600px;"/></td>
    <td><img src="https://lh3.googleusercontent.com/tvibZs0AAzKvE0B5t39gGUcsOga47C-Fnx2nnLiaERxSFPCQX-ZdPKBR1cKI8xSgaKqrwTCwE2guPvWZT1lvbWJJEA=s1280-w1280-h800" alt="Pairing Screen Screenshot" style="width: 100%; max-width: 600px;"/></td>
  </tr>
  <tr>
    <td><img src="https://lh3.googleusercontent.com/w4GUV-f_twURLcmYQqrENRvZ59GXFGGiW8wWsalwWW1Por54TbpX-o3Fwg8b1z6IJlwn8x20wTTsOkGTbCqsxlr0kw=s1600-w1600-h1000" alt="Demo Gesture Right" style="width: 100%; max-width: 600px;"/></td>
    <td><img src="https://lh3.googleusercontent.com/I6-zaEHLxCnGiUH7n6kwBQIZCJK7ZJdxBOJ7OVX1X7XAUGQGtNGDWVJMIUlS6-Z-hppxa5P0kVaQQ3EIH5_kBVOXPw=s1600-w1600-h1000" alt="Demo Gesture Right" style="width: 100%; max-width: 600px;"/></td>
  </tr>
</table>

## Getting Started
### Prerequisites 
- **Node.js and npm**: Required for setting up the frontend website. Download from [nodejs.org](https://nodejs.org/) , which includes npm. 
- **Python 3 and pip**: Needed for the backend server. Available for download at [python.org](https://python.org/) . 
- **Chromium Browser**: Necessary for installing and using the Chrome Extension.
### Installation Guide
#### cloning the repo
1. **Clone the Repository** : Obtain the HandGesture recognition codebase.

```shell
git clone https://github.com/xevansz/Handgesture-Recognition
cd Handgesture-Recognition
``` 
2. **Install Dependencies** : Get all required libraries.

```shell
pip3 install -r requirements.txt
```
3. **Running the project**

just run 
```shell
python3 gesture.py
```
### Using GesturePresenter

After running the script you will get a window popup. Adjusting the brightness of screen varies result. try to position hand completely in the box and avoid arm or wrist coming in the box. done using range values so may work for different color ranges for different people.

## Disclaimer



