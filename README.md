# auto-capture-selfie-using-smile-detection
This system automatically capture your photo by detecting your smile.
<br>
Author- Harvansh Singh
<br><br>
<u><b>test.py (Smile Detection Engine):</u></b>
<br>
Camera & AI Setup: Initializes webcam and loads pre-trained face/smile detection models<br>
Real-time Processing: Continuously captures video frames and analyzes them<br>
Smart Detection: Focuses smile detection on the mouth area of detected faces<br>
Timing Control: Prevents spam by enforcing 2-second intervals between captures<br>
File Management: Creates timestamped selfies in organized directory structure<br>
User Interface: Shows live detection status, rectangles around faces/smiles, and instructions<br>
Resource Management: Properly releases camera and closes windows on exit<br>
<br><br>
<u><b>main.py (GUI Application):</u></b>
<br>
Professional Interface: Creates attractive desktop application with images and buttons<br>
Image Handling: Loads interface images with fallback colored rectangles if files missing<br>
Thread Management: Runs camera script in background to prevent GUI freezing<br>
Error Handling: Comprehensive error checking with user-friendly messages<br>
Photo Gallery: Scrollable viewer showing all captured selfies with timestamps<br>
Status Updates: Real-time feedback showing application state and photo counts<br>
Cross-Directory Support: Finds photos in multiple possible locations<br>
<br><br>
Key Technical Concepts Explained:<br>
Threading: Prevents GUI freezing by running camera in separate thread<br>
Exception Handling: Try-catch blocks handle missing files, camera errors, etc.<br>
Directory Management: Automatic creation and organization of photo storage<br>
Image Processing: Resizing, format conversion, and display optimization<br>
Event-Driven Programming: GUI responds to button clicks and user interactions<br>
Process Management: Launching external scripts and monitoring their execution
The comments explain not just what the code does, but why each decision was made and how the components work together to create a complete application.
