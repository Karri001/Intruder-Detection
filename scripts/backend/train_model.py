import cv2
import os
import numpy as np
import sqlite3
import face_recognition

# === Paths ===
DB_PATH = r"C:\Users\VENKAT REDDY\Desktop\Intruder-Detection\database\faces.db"
IMAGE_DIR = r"C:\Users\VENKAT REDDY\Desktop\Intruder-Detection\database\images"

# Ensure image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Ensure database and table exist
def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS faces (id INTEGER PRIMARY KEY, name TEXT, encoding BLOB)")
        conn.commit()

initialize_database()

def capture_faces(person_name, num_images=50):
    """Captures multiple images of a person and stores them in a named folder"""
    person_dir = os.path.join(IMAGE_DIR, person_name)
    os.makedirs(person_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            continue

        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            count += 1
            file_path = os.path.join(person_dir, f"{count}.jpg")
            cv2.imwrite(file_path, frame)
            print(f"📸 Saved {file_path} ({count}/{num_images})")

        cv2.imshow("Capturing Faces", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ {count} images saved for {person_name}!")

def store_multiple_encodings():
    """Processes all stored images and saves multiple face encodings in the database"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        for person_name in os.listdir(IMAGE_DIR):
            person_path = os.path.join(IMAGE_DIR, person_name)
            if not os.path.isdir(person_path):
                continue

            for img_name in os.listdir(person_path):
                img_path = os.path.join(person_path, img_name)
                img = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(img)

                for encoding in encodings:
                    encoding_blob = np.array(encoding).tobytes()
                    cursor.execute(
                        "INSERT INTO faces (name, encoding) VALUES (?, ?)",
                        (person_name, encoding_blob)
                    )

        conn.commit()
        print("✅ Stored multiple encodings per person.")

def delete_person(person_name):
    """Deletes a person's images and face encodings from the database"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM faces WHERE name=?", (person_name,))
        conn.commit()
        print(f"🗑️ Deleted {person_name} from the database.")

    # Delete images from the directory
    person_dir = os.path.join(IMAGE_DIR, person_name)
    if os.path.exists(person_dir):
        for file in os.listdir(person_dir):
            os.remove(os.path.join(person_dir, file))
        os.rmdir(person_dir)
        print(f"🗑️ Deleted image directory for {person_name}.")
    else:
        print(f"⚠️ No image directory found for {person_name}.")

# === Main Program ===
if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Train new person")
        print("2. Delete a person")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            person_name = input("Enter the person's name: ").strip()
            capture_faces(person_name, num_images=50)
            store_multiple_encodings()

        elif choice == "2":
            person_name = input("Enter the name to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{person_name}'? (yes/no): ").lower()
            if confirm == "yes":
                delete_person(person_name)

        elif choice == "3":
            print("👋 Exiting program.")
            break

        else:
            print("❌ Invalid choice. Try again.")
