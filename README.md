# Sleeping Alert System

A computer vision application that monitors eye closure duration and alerts you when you're falling asleep. Perfect for students, drivers, or anyone who needs to stay awake during important tasks.

## Features

### Basic Features
- Real-time face and eye detection
- Eye Aspect Ratio (EAR) calculation to detect eye closure
- Continuous alerts until eyes are reopened
- Visual display of eye tracking and closure duration

### Advanced Features
- Face recognition for identifying specific users
- User profiles with personalized EAR thresholds and alert settings
- Statistics tracking for each user (drowsiness events, monitoring time)
- Primary user focus option for multi-person environments
- Detailed reports and visualization of drowsiness patterns

## Requirements

- Python 3.6+
- Webcam
- Libraries listed in requirements.txt

## Quick Setup

The easiest way to set up the application is to run the setup script:

```
python setup.py
```

This will:
1. Install all required packages
2. Download the facial landmark predictor model

## Demo Instructions

To quickly try the system:

1. **Setup**:
   ```
   python setup.py
   ```

2. **Create a User Profile**:
   ```
   python run_sleeping_alert.py --mode ui
   ```
   - Click "New User" and enter your name
   - Click "Capture Face" to start your webcam
   - When you see your face, click "Take Snapshot" to save your face data
   - Adjust your EAR Threshold if needed (0.25 is default)
   - Click "Save Changes"
   - If you want, set yourself as the primary user with "Set as Primary"
   - Close the UI window when done

3. **Run the Advanced System**:
   ```
   python run_sleeping_alert.py --mode advanced
   ```
   
4. **Test the System**:
   - Position yourself in front of the webcam
   - You should see your name displayed and a green rectangle around your face
   - Keep your eyes open for a few seconds
   - Close your eyes for more than 3 seconds
   - The alarm will sound and continue until you open your eyes
   - Try looking away, then back at the camera to test recognition
   - Press 'q' to quit

5. **View Your Statistics**:
   ```
   python run_sleeping_alert.py --mode ui
   ```
   - Click on the "Statistics" tab to see your drowsiness events

## Manual Setup

If you prefer to set up manually:

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```
2. Download the facial landmark predictor model:
   ```
   python download_model.py
   ```
   
   Or download it manually from one of these sources:
   - https://github.com/italojs/facial-landmarks-recognition/raw/master/shape_predictor_68_face_landmarks.dat
   - https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2 (needs extraction)

## Usage

### Launcher Script

The easiest way to use the system is with the launcher script:

```
python run_sleeping_alert.py [--mode {basic,advanced,ui}] [--focus-primary] [--tolerance TOLERANCE]
```

Options:
- `--mode`: Choose between basic alert system, advanced system with user profiles, or user interface
- `--focus-primary`: In advanced mode, only monitor the primary user
- `--tolerance`: Face recognition tolerance (0.4-0.8, lower is stricter)

### User Interface

To manage user profiles and settings:

```
python run_sleeping_alert.py --mode ui
```

Or directly:
```
python user_interface.py
```

The user interface allows you to:
- Create and manage user profiles
- Capture face images for recognition
- Set personalized thresholds for each user
- Set a primary user for focused monitoring
- View and generate statistics and reports

### Basic System

Run the basic drowsiness detection (no user profiles):
```
python run_sleeping_alert.py --mode basic
```

Or directly:
```
python sleeping_alert.py
```

### Advanced System

Run the advanced system with user profiles and recognition:
```
python run_sleeping_alert.py --mode advanced
```

Or directly:
```
python advanced_sleeping_alert.py [--focus-primary] [--tolerance TOLERANCE]
```

In advanced mode:
- The system will recognize users based on their face profiles
- Each user can have personalized detection thresholds
- Drowsiness events are recorded for each user
- The system can focus only on the primary user if desired

## How It Works

1. Detects face using dlib's frontal face detector
2. Identifies specific users with face recognition (advanced mode only)
3. Locates facial landmarks, specifically the eye regions
4. Calculates Eye Aspect Ratio (EAR) to determine if eyes are open or closed
5. Triggers a continuous alarm if eyes remain closed for the threshold duration
6. Stops the alarm when eyes are reopened
7. Records statistics for each user (advanced mode only)

## Statistics and Reporting

In advanced mode, the system tracks:
- Total monitoring time for each user
- Number of drowsiness events
- Timing patterns of drowsiness occurrences

Reports can be generated from the user interface or automatically when the application closes. Reports include:
- CSV summary of key statistics
- Visualizations of drowsiness patterns by day and hour

## Multi-Person Handling

When multiple people are visible in the camera:
- Basic mode: Monitors all faces, alerts if anyone's eyes are closed too long
- Advanced mode with focus on primary: Only monitors the primary user
- Advanced mode without focus: Monitors all recognized users, tracks statistics separately

## Customization

### Basic System Parameters
- `EYE_AR_THRESH`: Eye aspect ratio threshold (lower values are more sensitive)
- `EYE_AR_CONSEC_FRAMES_THRESHOLD`: Duration in seconds before alarm triggers
- `ALARM_SOUND_FREQ`: Frequency of alarm sound
- `ALARM_SOUND_DURATION`: Duration of alarm sound

### User Profile Customization
Each user can have personalized settings for:
- EAR threshold
- Duration threshold
- Recognition as primary user

### Face Recognition Settings
- Face recognition tolerance: Controls strictness of face matching
- Recognition frequency: How often face recognition is performed

## Files and Components

- `sleeping_alert.py`: Basic drowsiness detection
- `sleeping_alert_with_wav.py`: Basic system with WAV file support
- `advanced_sleeping_alert.py`: Advanced system with user recognition
- `user_management.py`: User profile and statistics management
- `user_interface.py`: GUI for managing users and settings
- `run_sleeping_alert.py`: Launcher script for all modes
- `setup.py`: Setup script for dependencies
- `download_model.py`: Helper script for downloading models

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses dlib for facial landmark detection
- Uses face_recognition library for face recognition
- Inspired by the need for drowsiness detection in various professional settings
