# Intruder-Detection

## 🚀 Overview
 The Intruder Detection System is an advanced AI-powered security solution designed to detect, identify, and alert against unauthorized intrusions in real time. By integrating Convolutional Neural Networks (CNNs) for facial recognition and multi-channel notifications, it offers a powerful, automated, and intelligent layer of protection for modern surveillance environments.

## Repository
This project is hosted on GitHub: [Intruder-Detection](https://github.com/Karri001/Intruder-Detection)

## 🧠 Key Features

**🎯 Smart Facial Recognition**: 
   - Uses CNN-based face embeddings to compare live video frames with authorized personnel.
   - Individuals with a similarity score < 0.6 are classified as intruders.
   - Pre-registered faces are explicitly excluded from intruder alerts.

**⚡ Real-Time Processing**:
   - Built with FastAPI, ensuring low-latency video frame analysis and rapid response times.

**💻 Intuitive Frontend**:
   - A clean HTML-based dashboard for live monitoring, system control, and event review.

**💾 Efficient Data Management**:
   - Authorized user embeddings stored in a .pkl file.
   - Profiles, access logs, and event data managed through SQLite for simplicity and reliability.

**📲 Multi-Channel Alerts**:
   - SMS notifications powered by Twilio API.
   - Email alerts with a captured PDF snapshot of the intruder.
   - Re-notification feature for continuous presence detection (if the intruder remains in view).

## ⚙️ How It Works
 The Intruder Detection System operates through a series of well-coordinated modules that work together in real time to detect, verify, and alert about unauthorized individuals.

**🧩 Step-by-Step Workflow**:

  1. **Live Video Capture**
     - The system continuously streams video from a connected camera.
     - Each frame is processed in real time by the backend running on FastAPI.

  2. **Face Detection & Preprocessing**:
     - Using OpenCV or a similar vision library, faces are detected within the frame.
     - Each detected face is cropped, aligned, and normalized to prepare it for embedding extraction.
     
  3. **Face Embedding Generation (CNN Model)**:
     - A Convolutional Neural Network (CNN) converts the processed face into a 128-dimensional embedding vector — a unique numerical representation of the face.
     - This embedding is compared to the database of authorized personnel embeddings stored in a .pkl file.

  4. **Identity Verification**:
     - The system calculates a similarity score (e.g., cosine similarity) between the detected face and each authorized embedding.
     - If the highest similarity < 0.6, the person is classified as an intruder.
     - If the face matches a registered embedding, the system marks the person as authorized and skips alerting.

  5. **Intruder Classification & Logging**:
     - Once an intruder is detected:
        - Their snapshot is saved locally.
        - Event details (timestamp, location, similarity score, image path) are stored in an SQLite database for record keeping.

  6. **Multi-Channel Alerting**:
     - The system immediately triggers alerts through:
        - 📩 Email — A detailed report containing an attached PDF snapshot of the intruder.
        - 📱 SMS — A concise text notification sent via Twilio API.
        - A re-notification mechanism re-alerts security staff if the same intruder remains visible for an extended duration.
     
  7. **Frontend Interaction**:
     - The HTML dashboard allows users to:
        - View live video streams.
        - Monitor detection logs.
        - Manage authorized personnel profiles.
        - Review and download captured intruder reports.


## 🔧 Setup and Installation
Follow these steps to set up the project:

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Karri001/Intruder-Detection.git
   cd Intruder-Detection
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Start Application:
   - Open Terminal with Project Directory and Use the below commands to Activate dlib310 environment:
        ```bash
      cd Intruder-Detection
      dlib310/Scripts/Activate
      ```
   - Now navigate to the root backend folder to run the Application use below commands:
        ```bash
      cd Scripts
      cd backend
      python main.py
      ```
 4. After this the User has to manually run the index.html file so that the interface can pop up and various actions like Register face,Delete face ,Start and Stop Detection etc actions can be performed


## Screenshots
### Home Interface 
![Home Interface](https://github.com/user-attachments/assets/54ca3d07-0e4e-43ae-bd6e-90fe95317d07)

### Register Users
<img width="1920" height="1080" alt="Screenshot (355)" src="https://github.com/user-attachments/assets/c886e056-36f9-447f-99e9-d3e2277399fb" />

<img width="1920" height="1080" alt="Screenshot (356)" src="https://github.com/user-attachments/assets/f50942c2-8a57-4b6b-9cc5-3db025dfdf84" />

<img width="1920" height="1080" alt="Screenshot (357)" src="https://github.com/user-attachments/assets/8d316810-7709-45d2-957d-8e569ccfeab0" />


### Home Interface (After Login)
![Home Interface (After Login)](https://github.com/user-attachments/assets/7cf5af7f-afe9-48fe-b6a6-ee782cdaab28)


### ChatBot
![ChatBot](https://github.com/user-attachments/assets/c773f4b0-cf7c-4cbc-b75f-106826d44ca8)


### Video Demonstration
https://github.com/user-attachments/assets/7356f82d-3bb9-4ece-a95c-cb65af8f6e07



## Future Enhancements
- Allow users to chat in different languages by integrating multilingual models or translation APIs.
- Build a cross-platform mobile app using React Native or Flutter for on-the-go mental health support.
- Add speech-to-text and text-to-speech capabilities so users can talk and listen instead of typing.
- Improve the UI with theme switching, larger fonts, and accessibility options for better user experience.
- Implement end-to-end encryption and anonymization to enhance user trust and data security.

## Contributions
Contributions are welcome! Feel free to fork the repository and submit pull requests with improvements or additional features.

## License
This project is licensed under the [MIT License](LICENSE).

---

**Author**: K.Sai Sri Venkata Reddy

For questions or suggestions, please contact: [venkatreddykarri001@gmail.com.com]
