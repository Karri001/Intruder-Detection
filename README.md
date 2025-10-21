# Intruder-Detection

## Overview
The Intruder Detection System is an advanced AI-powered security solution designed to detect, identify, and alert against unauthorized intrusions in real time. By integrating Convolutional Neural Networks (CNNs) for facial recognition and multi-channel notifications, it offers a powerful, automated, and intelligent layer of protection for modern surveillance environments.

## Repository
This project is hosted on GitHub: [Intruder-Detection](https://github.com/Karri001/Intruder-Detection)

## Features
- **Conversational AI (Ollama Integration)**: The chatbot uses Ollama’s local large language model as its “brain” to understand and respond naturally to user inputs.
- **Chat History**: Each user’s previous conversations are securely stored and retrievable, allowing continuity and personalization in future sessions.
- **User Authentication**:
  - Signup: Create a new account with secure credentials.
  - Login: Access personalized chat experiences.
  - Forgot Password: Reset password securely using email verification or token-based recovery.
- **Responsive UI**: Built with React, the interface is intuitive, user-friendly, and optimized for both desktop and mobile use.
- **Backend & Database**:
  - Python (Flask/FastAPI): Handles communication with Ollama, authentication, and chat data management.
  - MongoDB: Stores user data, chat histories, and authentication details.

## How It Works
1. **User Authentication**: 
   - Users sign up or log in using their email and password.
   - The system verifies credentials (stored securely in MongoDB) and creates a session using tokens.
2. **Chat Interface**: 
   - Once logged in, users access the chat screen built with React.
   - They can send messages to the chatbot through a simple, responsive UI.
3. **Backend Processing**: 
   - Each message is sent from the frontend to the Python backend (Flask/FastAPI).
   - The backend forwards the user’s input to Ollama, which serves as the AI “brain.”
4. **Ollama Response Generation**: 
   - Ollama processes the input using its local large language model.
   - It generates a natural, empathetic reply suitable for mental health support conversations.
5. **Chat History Management**: 
   - The backend stores both user messages and bot replies in MongoDB.
   - When users return, the chatbot loads their previous chat history for context and continuity.
6. **Optional Password Recovery**: 
   - If a user forgets their password, a secure token or email-based reset process is triggered.

## Setup and Installation
Follow these steps to set up the project:

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Karri001/Mental-Health-Chatbot.git
   cd Mental-Health-Chatbot
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Download Ollama:
   - Ollama can be downloaded from this site (https://ollama.com/download)
4. Open Three Different Terminals with the Project Folder location and Open the Three folders Shown Below in Those Terminals to Run the Application :
   - To Start Chatbot of the Application
    
      ```bash
      cd Cbot
      python app.py
      ```
   - To Start Frontend of the Application
    
      ```bash
      cd frontend
      npm start
      ```
   - To Start Backend of the Application
    
      ```bash
      cd backend
      npm start
      ```
5. The Application will Automatically launch itself after the Frontend has been launched and then the User can start Interacting with the ChatBot.


## Screenshots
### Home Interface (Befor Login)
![Home Interface (Befor Login)](https://github.com/user-attachments/assets/2377fe66-af50-4ecd-8315-b22eac9aec46)


### Login/SignUp Page
 - Login Page
  
 ![Login Page](https://github.com/user-attachments/assets/56e2236a-e121-4816-9565-c86585ad4020)
 - SignUp Page
   
 ![SignUp Page](https://github.com/user-attachments/assets/6358af57-1b66-46ec-9968-11895ac4cae0)


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
