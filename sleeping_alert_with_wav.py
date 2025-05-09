import cv2
import dlib
import numpy as np
import time
import winsound
import threading
import os
from scipy.spatial import distance as dist

# Initialize face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Constants
EYE_AR_THRESH = 0.25  # Eye Aspect Ratio threshold
EYE_AR_CONSEC_FRAMES_THRESHOLD = 2.0  # Time in seconds
ALARM_SOUND_PATH = "alarm.wav"  # Path to your alarm sound WAV file

# Global flag to control alarm looping
alarm_flag = False
alarm_thread = None

# Create a default alarm sound file if it doesn't exist
def create_default_alarm_file():
    if not os.path.exists(ALARM_SOUND_PATH):
        # If no alarm file exists, we'll use the beep function as a fallback
        print(f"Warning: {ALARM_SOUND_PATH} not found. Will use beep sound instead.")
        global sound_alarm_continuous
        sound_alarm_continuous = lambda: continuous_beep()
        return False
    return True

def continuous_beep():
    """Continuous beep as a fallback when no WAV file is available"""
    global alarm_flag
    alarm_flag = True
    
    while alarm_flag:
        winsound.Beep(2500, 1000)
        time.sleep(0.5)  # Small pause between beeps

# Define indices for the facial landmarks
# for the left and right eyes
LEFT_EYE_INDICES = list(range(36, 42))
RIGHT_EYE_INDICES = list(range(42, 48))

def calculate_ear(eye):
    """Calculate the Eye Aspect Ratio (EAR)"""
    # Compute the euclidean distances between the vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    
    # Compute the euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])
    
    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

def sound_alarm_continuous():
    """Play an alarm sound from WAV file continuously until eyes open"""
    global alarm_flag
    alarm_flag = True
    
    while alarm_flag:
        winsound.PlaySound(ALARM_SOUND_PATH, winsound.SND_FILENAME)
        # If PlaySound finishes and alarm_flag is still True, loop again

def stop_alarm():
    """Stop the alarm"""
    global alarm_flag, alarm_thread
    alarm_flag = False
    if alarm_thread is not None and alarm_thread.is_alive():
        alarm_thread.join(1.0)  # Wait for thread to finish with timeout

def main():
    global alarm_thread
    
    # Check if alarm sound file exists, otherwise use beep
    has_alarm_file = create_default_alarm_file()
    
    cap = cv2.VideoCapture(0)  # Initialize webcam
    
    if not cap.isOpened():
        print("Could not open webcam")
        return
    
    print("Sleeping Alert System Started. Press 'q' to quit.")
    
    # Initialize variables for tracking eye closure duration
    eyes_closed_start_time = None
    alarm_on = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        # Resize frame for faster processing
        frame = cv2.resize(frame, (640, 480))
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = detector(gray)
        
        # If no faces are detected and alarm is on, keep showing alert
        if len(faces) == 0 and alarm_on:
            cv2.putText(frame, "WAKE UP ALERT!", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        for face in faces:
            # Get facial landmarks
            landmarks = predictor(gray, face)
            
            # Extract left and right eye coordinates
            left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) 
                                for i in LEFT_EYE_INDICES])
            right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) 
                                 for i in RIGHT_EYE_INDICES])
            
            # Calculate EAR for both eyes
            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            
            # Average EAR of both eyes
            ear = (left_ear + right_ear) / 2.0
            
            # Visualize eye contours
            cv2.drawContours(frame, [cv2.convexHull(left_eye)], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [cv2.convexHull(right_eye)], -1, (0, 255, 0), 1)
            
            # Display EAR value
            cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Check if eyes are closed
            if ear < EYE_AR_THRESH:
                if eyes_closed_start_time is None:
                    eyes_closed_start_time = time.time()
                
                # Calculate how long eyes have been closed
                elapsed_time = time.time() - eyes_closed_start_time
                
                # Display eye closure duration
                cv2.putText(frame, f"Eyes Closed: {elapsed_time:.1f}s", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Check if eyes have been closed for enough time to trigger alarm
                if elapsed_time >= EYE_AR_CONSEC_FRAMES_THRESHOLD and not alarm_on:
                    alarm_on = True
                    # Play alarm in a separate thread that continues until eyes open
                    alarm_thread = threading.Thread(target=sound_alarm_continuous)
                    alarm_thread.daemon = True  # Make thread daemon so it exits with the program
                    alarm_thread.start()
                    
                    # Display ALERT on screen
                    cv2.putText(frame, "WAKE UP ALERT!", (10, 90),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                # Reset if eyes are open
                eyes_closed_start_time = None
                
                # If eyes are now open and alarm is on, turn it off
                if alarm_on:
                    alarm_on = False
                    stop_alarm()
        
        # Show the frame
        cv2.imshow("Sleeping Alert System", frame)
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Make sure to stop the alarm and clean up
    stop_alarm()
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 