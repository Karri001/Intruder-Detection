import cv2
import sqlite3
import numpy as np
import face_recognition
import threading
import time
from send_alert import send_alert

# Database & Intruder Image Path
DB_PATH = r"C:\Users\VENKAT REDDY\Desktop\Intruder-Detection\database\faces.db"
INTRUDER_IMAGE_PATH = r"C:\Users\VENKAT REDDY\Desktop\Intruder-Detection\intruder.jpg"

# Load stored face encodings
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name, encoding FROM faces")
stored_faces = cursor.fetchall()

known_encodings = []
known_names = []

for name, encoding_blob in stored_faces:
    encoding = np.frombuffer(encoding_blob, dtype=np.float64)
    known_encodings.append(encoding)
    known_names.append(name)

print(f"✅ Loaded {len(known_names)} known faces from database.")

# Parameters
THRESHOLD = 0.45
FRAME_BUFFER_SIZE = 5
INTRUDER_ALERT_DELAY = 2  # seconds of continuous detection before first alert
INTRUDER_REPEAT_ALERT_INTERVAL = 10  # seconds between repeated alerts after first

face_history = {}
intruder_track = {}

# Load OpenCV Haar cascade for fallback detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def preprocess_frame(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    # Convert back to BGR
    sharpened_bgr = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)
    # Histogram equalization on L channel in LAB color space for contrast
    lab = cv2.cvtColor(sharpened_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    lab = cv2.merge((l,a,b))
    enhanced_frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return enhanced_frame

def detect_faces_opencv(gray_frame):
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
    locations = []
    for (x, y, w, h) in faces:
        # Convert to (top, right, bottom, left)
        locations.append((y, x+w, y+h, x))
    return locations

def get_face_center(location):
    top, right, bottom, left = location
    return ((left + right) // 2, (top + bottom) // 2)

def is_same_face(center1, center2, max_distance=50):
    return np.linalg.norm(np.array(center1) - np.array(center2)) < max_distance

def recognize_face(frame):
    processed_frame = preprocess_frame(frame)
    rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

    # Try CNN face detection
    face_locations = face_recognition.face_locations(rgb_frame, model="cnn")

    # If no faces found, fallback to OpenCV detector
    if len(face_locations) == 0:
        gray_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2GRAY)
        face_locations = detect_faces_opencv(gray_frame)

    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    current_time = time.time()

    detected_this_frame = []

    for face_encoding, face_location in zip(face_encodings, face_locations):
        center = get_face_center(face_location)

        matched_key = None
        for key in face_history.keys():
            if is_same_face(center, key):
                matched_key = key
                break

        if matched_key is None:
            matched_key = center
            face_history[matched_key] = []

        face_history[matched_key].append(face_encoding)
        if len(face_history[matched_key]) > FRAME_BUFFER_SIZE:
            face_history[matched_key].pop(0)

        avg_encoding = np.mean(face_history[matched_key], axis=0)

        if known_encodings:
            face_distances = face_recognition.face_distance(known_encodings, avg_encoding)
            best_match_index = np.argmin(face_distances)
            confidence = 1 - face_distances[best_match_index]

            if face_distances[best_match_index] < THRESHOLD:
                name = known_names[best_match_index]
            else:
                name = "INTRUDER"
        else:
            name = "INTRUDER"
            confidence = 0

        top, right, bottom, left = face_location
        color = (0, 255, 0) if name != "INTRUDER" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, f"{name} ({confidence:.2f})", (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        detected_this_frame.append(matched_key)

        # Intruder alert logic with repeated alerts
        if name == "INTRUDER":
            if matched_key not in intruder_track:
                intruder_track[matched_key] = {
                    'first_detected_time': current_time,
                    'last_alert_time': 0,
                    'alerted': False
                }
            else:
                elapsed_since_first = current_time - intruder_track[matched_key]['first_detected_time']
                elapsed_since_last_alert = current_time - intruder_track[matched_key]['last_alert_time']

                # First alert after delay
                if elapsed_since_first >= INTRUDER_ALERT_DELAY and not intruder_track[matched_key]['alerted']:
                    print("🚨 INTRUDER DETECTED! Sending alert...")
                    cv2.imwrite(INTRUDER_IMAGE_PATH, frame)
                    threading.Thread(target=send_alert, args=(INTRUDER_IMAGE_PATH,)).start()
                    intruder_track[matched_key]['alerted'] = True
                    intruder_track[matched_key]['last_alert_time'] = current_time

                # Repeat alert every INTRUDER_REPEAT_ALERT_INTERVAL seconds
                elif intruder_track[matched_key]['alerted'] and elapsed_since_last_alert >= INTRUDER_REPEAT_ALERT_INTERVAL:
                    print("🚨 INTRUDER STILL PRESENT! Sending repeated alert...")
                    cv2.imwrite(INTRUDER_IMAGE_PATH, frame)
                    threading.Thread(target=send_alert, args=(INTRUDER_IMAGE_PATH,)).start()
                    intruder_track[matched_key]['last_alert_time'] = current_time
        else:
            if matched_key in intruder_track:
                del intruder_track[matched_key]

    # Cleanup faces not detected this frame
    keys_to_remove = [key for key in face_history if key not in detected_this_frame]
    for key in keys_to_remove:
        face_history.pop(key, None)
        intruder_track.pop(key, None)

    return frame

def detect_intruder():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ ERROR: Camera could not be opened.")
        return

    print("📷 Camera started. Press 'Q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ ERROR: Frame could not be read from camera.")
            break

        frame = recognize_face(frame)
        cv2.imshow("Intruder Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_intruder()
conn.close()
