# Import required libraries
import cv2         # OpenCV for computer vision tasks (camera, image processing, face/smile detection)
import time        # For timestamps and timing control
import numpy as np # NumPy for numerical operations (though not heavily used in this script)
import os          # Operating system interface for file/directory operations

def main():
    """
    Main function that runs the complete smile detection and selfie capture system.
    
    This function:
    1. Loads pre-trained AI models for detecting faces and smiles
    2. Opens the webcam for real-time video capture
    3. Processes each video frame to detect faces and smiles
    4. Automatically captures and saves selfies when a smile is detected
    5. Provides visual feedback and user interface elements
    
    Returns:
        bool: True if the application ran successfully, False if there were errors
    """
    
    # STEP 1: LOAD PRE-TRAINED AI MODELS (Haar Cascades)
    # These are machine learning models that can detect specific patterns in images
    
    # Get the full path to the face detection model file
    # cv2.data.haarcascades contains the directory where OpenCV stores these models
    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    
    # Get the full path to the smile detection model file
    smile_cascade_path = cv2.data.haarcascades + 'haarcascade_smile.xml'

    # Load the AI models into memory
    # CascadeClassifier is OpenCV's class for using Haar cascade models
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    smile_cascade = cv2.CascadeClassifier(smile_cascade_path)

    # Verify that both models loaded successfully
    # empty() returns True if the model failed to load
    if face_cascade.empty() or smile_cascade.empty():
        print("Error: Unable to load Haar cascade files. Please check your OpenCV installation.")
        return False  # Exit the function if models can't be loaded

    # STEP 2: INITIALIZE CAMERA
    # VideoCapture(0) opens the default camera (usually built-in webcam)
    # The parameter 0 refers to the first camera device
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Unable to access the camera. Please check your webcam.")
        return False

    # STEP 3: CONFIGURE CAMERA SETTINGS FOR OPTIMAL PERFORMANCE
    # Set camera resolution to 640x480 pixels (good balance of quality and speed)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Set frame rate to 30 frames per second for smooth video
    cap.set(cv2.CAP_PROP_FPS, 30)

    # STEP 4: INITIALIZE VARIABLES FOR TIMING AND PHOTO MANAGEMENT
    last_saved_time = 0    # Timestamp of when the last selfie was saved
    save_interval = 2      # Minimum seconds between consecutive selfie captures (prevents spam)
    
    # Create a dedicated directory for storing selfies
    selfie_dir = "selfies"
    if not os.path.exists(selfie_dir):
        os.makedirs(selfie_dir)  # Create the directory if it doesn't exist
    
    # STEP 5: DISPLAY STARTUP MESSAGES
    print("Smile detection started! Press 'q' to quit.")
    print("Make sure to smile for the camera to capture selfies!")
    
    try:
        # STEP 6: MAIN VIDEO PROCESSING LOOP
        # This loop runs continuously, processing each frame from the camera
        while True:
            # STEP 6A: CAPTURE A FRAME FROM THE CAMERA
            # ret = return value (True if frame captured successfully, False otherwise)
            # frame = the actual image data captured from the camera
            ret, frame = cap.read()
            
            # If frame capture failed, exit the loop
            if not ret:
                print("Error: Unable to read from the camera.")
                break

            # STEP 6B: PREPARE THE FRAME FOR FACE DETECTION
            # Convert color image to grayscale because Haar cascades work on grayscale images
            # This also improves processing speed significantly
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # STEP 6C: DETECT FACES IN THE CURRENT FRAME
            # detectMultiScale() scans the image for face patterns at different sizes and positions
            faces = face_cascade.detectMultiScale(
                gray_frame,         # The grayscale image to scan
                scaleFactor=1.1,    # How much the image size is reduced at each scale (1.1 = 10% reduction)
                minNeighbors=5,     # How many neighbors each candidate rectangle should retain (higher = more strict)
                minSize=(100, 100)  # Minimum possible face size in pixels (filters out very small detections)
            )

            # STEP 6D: PROCESS EACH DETECTED FACE
            # faces is a list of rectangles, each representing a detected face
            # Each rectangle is defined as (x, y, width, height)
            for (x, y, w, h) in faces:
                
                # STEP 6D-i: DRAW VISUAL INDICATORS FOR THE DETECTED FACE
                # Draw a green rectangle around the detected face for user feedback
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Parameters: (image, top-left corner, bottom-right corner, color (B,G,R), thickness)
                
                # Add a text label above the face rectangle
                cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                # Parameters: (image, text, position, font, scale, color, thickness)

                # STEP 6D-ii: DEFINE REGION OF INTEREST (ROI) FOR SMILE DETECTION
                # Focus on the lower 2/3 of the face where the mouth is located
                # This improves smile detection accuracy and reduces false positives
                roi_gray = gray_frame[y + int(h/3):y + h, x:x + w]  # Grayscale ROI for detection
                roi_color = frame[y + int(h/3):y + h, x:x + w]      # Color ROI for drawing rectangles

                # STEP 6D-iii: DETECT SMILES WITHIN THE FACE ROI
                # Only look for smiles in the mouth area of detected faces
                smiles = smile_cascade.detectMultiScale(
                    roi_gray,           # The grayscale mouth region to scan
                    scaleFactor=1.8,    # More aggressive scaling for smile detection
                    minNeighbors=20,    # Higher threshold for smile confidence (reduces false positives)
                    minSize=(20, 20)    # Minimum smile size in pixels
                )
                
                # STEP 6D-iv: PROVIDE DEBUG INFORMATION
                # Print detection status to console for debugging and monitoring
                print(f"Face detected at ({x},{y}), Smiles found: {len(smiles)}", end="")
                
                # STEP 6D-v: HANDLE SMILE DETECTION RESULTS
                if len(smiles) > 0:
                    # SMILE DETECTED - Process the positive detection
                    
                    # Draw red rectangles around detected smile regions for visual feedback
                    for (sx, sy, sw, sh) in smiles:
                        cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)
                    
                    # Display "SMILE DETECTED!" message on the video feed
                    cv2.putText(frame, 'SMILE DETECTED!', (x, y + h + 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    
                    # STEP 6D-v-a: CHECK TIMING CONSTRAINTS
                    # Prevent rapid-fire selfie captures by enforcing a minimum time interval
                    current_time = time.time()  # Get current timestamp
                    time_since_last = current_time - last_saved_time
                    
                    if time_since_last > save_interval:
                        # ENOUGH TIME HAS PASSED - CAPTURE AND SAVE SELFIE
                        
                        # Call the selfie saving function
                        success = save_selfie(frame, selfie_dir)
                        
                        if success:
                            # Selfie saved successfully
                            last_saved_time = current_time  # Update timestamp
                            
                            # Show visual confirmation on screen
                            cv2.putText(frame, 'SELFIE SAVED!', (50, 50), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                            print(" -> Selfie saved!")
                        else:
                            # Selfie saving failed
                            print(" -> Failed to save selfie")
                    else:
                        # NOT ENOUGH TIME HAS PASSED - SHOW COUNTDOWN
                        remaining_time = save_interval - time_since_last
                        
                        # Display countdown timer on screen
                        cv2.putText(frame, f'Wait {remaining_time:.1f}s', (x, y + h + 60), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                        print(f" -> Waiting {remaining_time:.1f}s")
                else:
                    # NO SMILE DETECTED - Encourage user to smile
                    cv2.putText(frame, 'Please smile!', (x, y + h + 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                    print(" -> No smile")

            # STEP 6E: ADD USER INTERFACE ELEMENTS TO THE VIDEO FRAME
            # Display instructions for quitting the application
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display count of saved selfies (live counter)
            cv2.putText(frame, f"Selfies saved: {count_selfies(selfie_dir)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # STEP 6F: DISPLAY THE PROCESSED VIDEO FRAME
            # Show the video feed with all annotations and rectangles
            cv2.imshow('Smile Detection - Selfie Camera', frame)

            # STEP 6G: CHECK FOR USER INPUT (KEYBOARD CONTROLS)
            # waitKey(1) waits for keyboard input for 1 millisecond
            # 0xFF masks the result to get only the lower 8 bits
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                # User pressed 'q' to quit
                print("\nExiting smile detection...")
                break
            elif key == ord('s'):
                # User pressed 's' for manual selfie capture (bonus feature)
                save_selfie(frame, selfie_dir)
                print("Manual selfie saved!")

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nInterrupted by user")
    except Exception as e:
        # Handle any unexpected errors
        print(f"\nUnexpected error: {e}")
    finally:
        # STEP 7: CLEANUP RESOURCES (ALWAYS EXECUTES)
        # This cleanup code runs whether the program exits normally or due to an error
        print("Cleaning up resources...")
        
        # Release the camera so other applications can use it
        cap.release()
        
        # Close all OpenCV windows
        cv2.destroyAllWindows()
        print("Cleanup complete!")

    return True  # Indicate successful completion


def save_selfie(image, directory="selfies"):
    """
    Save the current video frame as a selfie image with timestamp.
    
    This function:
    1. Creates a unique filename using current date and time
    2. Saves the image to the specified directory
    3. Provides error handling and user feedback
    
    Args:
        image: The video frame (numpy array) to save as an image
        directory: Directory path where the selfie should be saved
    
    Returns:
        bool: True if the selfie was saved successfully, False if there was an error
    """
    try:
        # STEP 1: CREATE UNIQUE FILENAME WITH TIMESTAMP
        # strftime formats the current time as: YYYYMMDD-HHMMSS
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"selfie_{timestamp}.png"
        
        # Create the full file path by joining directory and filename
        file_path = os.path.join(directory, file_name)
        
        # STEP 2: SAVE THE IMAGE FILE
        # imwrite() saves the image array to disk as a PNG file
        # Returns True if successful, False if failed
        success = cv2.imwrite(file_path, image)
        
        # STEP 3: PROVIDE USER FEEDBACK
        if success:
            print(f"Selfie saved as {file_path}")
            return True
        else:
            print("Failed to save image")
            return False
            
    except Exception as e:
        # Handle any file system or permission errors
        print(f"Error saving selfie: {e}")
        return False


def count_selfies(directory="selfies"):
    """
    Count the total number of selfie files in the specified directory.
    
    This function is used to display a running count of captured selfies.
    
    Args:
        directory: The directory to search for selfie files
    
    Returns:
        int: The number of selfie files found (files starting with 'selfie_' and ending with '.png')
    """
    try:
        # Check if the directory exists
        if not os.path.exists(directory):
            return 0
        
        # List all files in the directory and filter for selfie files
        # Use list comprehension to count files matching our naming pattern
        return len([f for f in os.listdir(directory) 
                   if f.startswith('selfie_') and f.endswith('.png')])
    except:
        # Return 0 if there's any error accessing the directory
        return 0


def test_smile_detection():
    """
    Test function to verify that smile detection is working properly.
    
    This is a debugging tool that:
    1. Tests the smile detection system in isolation
    2. Provides frame-by-frame detection statistics
    3. Helps troubleshoot detection issues
    
    This function can be used independently to verify that:
    - The camera is working
    - Face detection is functioning
    - Smile detection is responsive
    
    Returns:
        bool: True if test completed successfully, False if there were errors
    """
    print("Testing smile detection...")
    
    # STEP 1: LOAD THE DETECTION MODELS
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    
    # Verify models loaded successfully
    if face_cascade.empty() or smile_cascade.empty():
        print("Error loading cascades")
        return False
    
    # STEP 2: INITIALIZE CAMERA
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error opening camera")
        return False
    
    print("Show your face and smile to test detection. Press 'q' to quit test.")
    
    try:
        # STEP 3: RUN TEST FOR LIMITED NUMBER OF FRAMES
        for i in range(50):  # Test for 50 frames only
            ret, frame = cap.read()
            if not ret:
                continue  # Skip failed frames
                
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
            
            # For each face, test smile detection
            for (x, y, w, h) in faces:
                # Focus on mouth area (lower 2/3 of face)
                roi_gray = gray[y + int(h/3):y + h, x:x + w]
                smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20, minSize=(20, 20))
                
                # Print detection statistics for debugging
                print(f"Frame {i}: {len(faces)} faces, {len(smiles)} smiles")
                
                # Allow early exit during testing
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break
                    
    finally:
        # STEP 4: CLEANUP TEST RESOURCES
        cap.release()
        cv2.destroyAllWindows()
    
    print("Test complete!")
    return True


# MAIN PROGRAM ENTRY POINT
if __name__ == "__main__":
    # This block only runs when the script is executed directly (not imported)
    
    # UNCOMMENT THE NEXT LINE TO RUN DETECTION TEST FIRST
    # test_smile_detection()
    
    # Run the main smile detection application
    success = main()
    
    # Provide final status message
    if success:
        print("Application completed successfully!")
    else:
        print("Application encountered errors.")