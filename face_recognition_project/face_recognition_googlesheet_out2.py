#################################################################################################
# A product developed by Ajai Raj and licensed under Iolinked.com
#################################################################################################

import cv2
import face_recognition
import os
import numpy as np
from collections import defaultdict
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
GSHEET_NAME = "face_detection_log"  # <-- Your Google Sheet name
SERVICE_ACCOUNT_FILE = "service_account.json"  # <-- Ensure this file is in the same directory

def load_known_faces(known_faces_dir):
    """Load and encode known faces from directory structure
    Expected structure:
    known_faces/        person1_name/
            image1.jpg
            image2.jpg
            ...
        person2_name/
            image1.jpg
            ...
    """
    known_faces = defaultdict(list) # is a special dictionary from pythons collections module
    # that automatically creates a new empty list when you try to access a key that doesn't exist
    #known_faces is a dictionary that maps person names to lists of face encodings 
    # KEY: person name
    # VALUE: list of face encodings
    """
    known_faces = {
    "ajai": [encoding1, encoding2, encoding3],  # List of face encodings from John's photos
    "sara": [encoding1, encoding2],            # List of face encodings from Sarah's photos
    }
    # With regular dictionary
    regular_dict = {}
    regular_dict["John"].append(encoding)  # Error! KeyError: 'John'

    # With defaultdict(list)
    known_faces = defaultdict(list)
    known_faces["John"].append(encoding)    # Works! Automatically creates empty list for "John"
    """
    
    # Check if directory exists
    if not os.path.exists(known_faces_dir):
        print(f"Directory {known_faces_dir} not found!")
        return {}
        
    # Iterate through each person's directory
    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if not os.path.isdir(person_dir):
            continue
            
        # Load each image for this person
        for image_file in os.listdir(person_dir):
            if not image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            image_path = os.path.join(person_dir, image_file)
            try:
                # Load and encode face
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                
                if not face_encodings:
                    print(f"No face found in {image_path}")
                    continue
                    
                # Add the first found face encoding
                known_faces[person_name].append(face_encodings[0])
                print(f"Loaded face from {image_path}")
                
            except Exception as e:
                print(f"Error loading {image_path}: {str(e)}")
                
    return known_faces


def init_gsheet(sheet_name, creds_path):
    """Initialize and return the Google Sheet object."""
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    # If empty, add headers
    if not sheet.get_all_values():
        sheet.append_row(["Name", "Timestamp", "Access"])
    return sheet


def append_gsheet_log(sheet, name, access):
    """Append a detection event to the Google Sheet."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([name, timestamp, access])

def main():
    # Initialize video capture (0 is usually the built-in webcam)
    video_capture = cv2.VideoCapture(0)

    # Load known faces with absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    known_faces_dir = os.path.join(script_dir, "known_faces")
    known_faces = load_known_faces(known_faces_dir)

    # Google Sheets log setup
    creds_path = os.path.join(script_dir, SERVICE_ACCOUNT_FILE)
    sheet = init_gsheet(GSHEET_NAME, creds_path)
    
    if not known_faces:
        print("No known faces found! Please add person folders with training images")
        print("Expected structure:")
        print("known_faces/")
        print("    person1_name/")
        print("        image1.jpg")
        print("        image2.jpg")
        print("    person2_name/")
        print("        image1.jpg")
        return

    print(f"Loaded {len(known_faces)} people:")
    for person, encodings in known_faces.items():
        print(f"- {person}: {len(encodings)} training images")

    ajai_raj_detected = False  # Track if Ajai_Raj is currently detected
    access_granted = False    # Track if any known face is detected
    access_denied = False     # Track if only unknown faces are detected
    special_access_granted = False  # Track if Ajai_Raj is detected

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Find all face locations in the current frame
        face_locations = face_recognition.face_locations(frame)
        # Get face encodings for any faces in the frame
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        detected_names = set()
        # Loop through each face in this frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            confidence = 0
            
            # Check against each person's face encodings
            for person_name, person_encodings in known_faces.items():
                # Compare against all training images for this person
                matches = face_recognition.compare_faces(person_encodings, face_encoding, tolerance=0.6)
                if True in matches:
                    # Calculate the confidence based on percentage of matching training images
                    match_confidence = matches.count(True) / len(matches)
                    if match_confidence > confidence:
                        confidence = match_confidence
                        name = person_name

            detected_names.add(name)
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with the name and confidence below the face
            label = f"{name} ({confidence*100:.0f}%)" if name != "Unknown" else name
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)

        # Access control logic
        if detected_names:
            if all(n == "Unknown" for n in detected_names):
                if not access_denied:
                    print("Access Denied")
                    access_denied = True
                    access_granted = False
                    special_access_granted = False
                    # Log each unknown detection
                    for n in detected_names:
                        append_gsheet_log(sheet, n, "Access Denied")
            elif "Ajai_Raj" in detected_names:
                if not special_access_granted:
                    print("Ajai_Raj: Special Access Granted")
                    special_access_granted = True
                    access_granted = False
                    access_denied = False
                    # Log Ajai_Raj detection
                    for n in detected_names:
                        if n == "Ajai_Raj":
                            append_gsheet_log(sheet, n, "Special Access Granted")
                        else:
                            append_gsheet_log(sheet, n, "Access Granted")
            else:
                if not access_granted:
                    print("Access Granted")
                    access_granted = True
                    access_denied = False
                    special_access_granted = False
                    # Log each known detection
                    for n in detected_names:
                        if n != "Unknown":
                            append_gsheet_log(sheet, n, "Access Granted")
                        else:
                            append_gsheet_log(sheet, n, "Access Denied")
        else:
            # No faces detected, reset all
            access_granted = False
            access_denied = False
            special_access_granted = False

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 