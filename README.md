# Visitor Recognition System

This is a **Visitor Recognition System** that uses face recognition technology and voice interaction to identify and manage visitors. The system is integrated with Firebase to store visitor information, including photos and mobile numbers.

## Features

- **Face Recognition:** Detects and recognizes faces using the `face_recognition` library.
- **Speech Recognition:** Interacts with visitors using voice commands to gather their information.
- **Firebase Integration:** Stores and retrieves visitor information from Firebase Realtime Database.
- **Graphical User Interface:** A Tkinter-based GUI to display visitor photos and details.
- **Real-time Notifications:** Greet recognized visitors with personalized messages.

## Installation

To run this project locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/Visitor-Recognition-System.git
   cd Visitor-Recognition-System
   
Install the Required Libraries:
pip install -r requirements.txt

Setup Firebase:
cred = credentials.Certificate("path_to_your_firebase_adminsdk.json")

Run the Application:
python visitor_recognition.py

Usage
Face Recognition: The system captures frames from the webcam and checks for known faces. If a recognized face is found, it greets the visitor. Otherwise, it prompts the visitor to provide their name and mobile number via voice input.

Firebase Storage: The captured visitor photo, along with their name and mobile number, is stored in Firebase.

Search Functionality: Users can search for a visitor by name, and the system will display the visitor's photo and mobile number if found.

Dependencies
The project uses the following libraries:

opencv-python
face_recognition
numpy
pyttsx3
speechrecognition
firebase-admin
keras
pillow
These dependencies are listed in the requirements.txt file.



