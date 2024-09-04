#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import cv2
import face_recognition
import numpy as np
import pyttsx3
from datetime import datetime
import speech_recognition as sr
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, db
from keras.models import model_from_json
import tkinter as tk
from PIL import Image, ImageTk
import base64
import time  # Add this import for time tracking

# Initialize Firebase Admin SDK only if it's not already initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK with provided JSON file and URL
    cred = credentials.Certificate("E:/res1-7cda9-firebase-adminsdk-i38sr-4b91829e4d.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://res1-7cda9-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })


# Initialize the text-to-speech engine with a specific rate
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the rate as needed (150 is just an example)

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Create a Tkinter window
root = tk.Tk()
root.title("Visitor Recognition System")
root.geometry("800x600")  # Set window size
root.config(bg="#f5f5f5")  # Set background color

# Function to fetch and display photos from Firebase Realtime Database
def display_photos():
    try:
        # Reference to the Firebase Realtime Database
        ref = db.reference('/visitors2')
        photos = ref.get()

        # Display photos in the GUI
        for i, (visitor_id, visitor_data) in enumerate(photos.items()):
            # Convert binary data from Firebase to image
            image_data = Image.open(BytesIO(base64.b64decode(visitor_data['photo'])))  # Decode base64 string
            image_data.thumbnail((150, 150))  # Resize image
            photo_tk = ImageTk.PhotoImage(image_data)
            label_photo = tk.Label(photo_frame, image=photo_tk, bg="#fff")
            label_photo.grid(row=i, column=0, padx=10, pady=10)

            # Retrieve visitor's name and mobile number from Firebase
            visitor_name = visitor_data['name']
            visitor_mobile = visitor_data['mobile_number']
            label_name = tk.Label(photo_frame, text=f"Name: {visitor_name}", bg="#fff")
            label_name.grid(row=i, column=1, padx=10, pady=10)
            label_mobile = tk.Label(photo_frame, text=f"Mobile: {visitor_mobile}", bg="#fff")
            label_mobile.grid(row=i, column=2, padx=10, pady=10)

            # Prevent garbage collection of PhotoImage objects
            label_photo.photo = photo_tk

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to speak a given text
def speak(text):
    print(f"Bot: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to get user's name, mobile number, and address through voice input
def get_visitor_info():
    current_time = datetime.now().time()

    if current_time.hour < 12:
        greet_message = "Good morning! Welcome to our Eduletics international school."
    elif 12 <= current_time.hour < 18:
        greet_message = "Good afternoon! Welcome to our Eduletics international school."
    else:
        greet_message = "Good evening! Welcome to our Eduletics international school."

    speak(greet_message)
    speak("May I know your name?")
    print("Listening for name...")

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=30)  # Increase timeout to 10 seconds
            visitor_name = recognizer.recognize_google(audio).lower()
            print(f"Visitor's name: {visitor_name}")
            speak("Could you please provide your mobile number?")
            print("Listening for mobile number...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=30)  # Wait for a longer period for mobile number
            visitor_mobile = recognizer.recognize_google(audio).lower()

            # Extract digits from recognized text to get mobile number
            visitor_mobile = ''.join(filter(str.isdigit, visitor_mobile))

            print(f"Visitor's mobile number: {visitor_mobile}")

            # Validate the mobile number
            if len(visitor_mobile) != 10:
                speak("Sorry, the mobile number you provided is invalid. Please provide a 10-digit mobile number.")
                return get_visitor_info()

            return visitor_name, visitor_mobile
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try again.")
        return get_visitor_info()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None, None

# Function to search and display photo and mobile number by name
def search_photo():
    try:
        name_to_search = entry_search.get().strip().lower()

        if name_to_search:
            # Reference to the Firebase Realtime Database
            ref = db.reference('/visitors2')
            photos = ref.get()

            # Search for the photo and mobile number associated with the searched name
            for visitor_id, visitor_data in photos.items():
                if visitor_data['name'].lower() == name_to_search:
                    # Convert binary data from Firebase to image
                    image_data = Image.open(BytesIO(base64.b64decode(visitor_data['photo'])))  # Decode base64 string
                    image_data.thumbnail((150, 150))  # Resize image
                    photo_tk = ImageTk.PhotoImage(image_data)
                    label_photo_search.config(image=photo_tk)
                    label_photo_search.photo = photo_tk

                    # Display visitor's mobile number
                    visitor_mobile = visitor_data['mobile_number']
                    label_mobile_search.config(text=f"Mobile: {visitor_mobile}")
                    break
            else:
                # Display a message if no photo found for the searched name
                label_photo_search.config(image='')
                label_photo_search.photo = None
                label_mobile_search.config(text="Mobile: Not found")
                speak(f"No photo found for {name_to_search}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Frame for search functionality
search_frame = tk.Frame(root, bg="#f5f5f5")
search_frame.pack(pady=20)

# Add Entry widget for user to input the name
entry_search = tk.Entry(search_frame, width=30, bd=2, relief=tk.FLAT)
entry_search.grid(row=0, column=0, padx=10)

# Add Button widget to trigger search action
button_search = tk.Button(search_frame, text="Search", command=search_photo, bg="#4285F4", fg="white", bd=0)
button_search.grid(row=0, column=1, padx=10)

# Add Label widget to display the photo of the searched person
label_photo_search = tk.Label(root, bg="#f5f5f5")
label_photo_search.pack(pady=20)

# Add Label widget to display the mobile number of the searched person
label_mobile_search = tk.Label(root, text="Mobile:", bg="#f5f5f5", font=("Arial", 12))
label_mobile_search.pack()

# Create a frame for the photo display
photo_frame = tk.Frame(root, bg="#fff")
photo_frame.pack(pady=20)

try:
    # Load Anti-Spoofing Model
    json_file_spoof = open(r"E:\antispoofing_model.json")  # Replace with the actual path
    loaded_model_json_spoof = json_file_spoof.read()
    json_file_spoof.close()

    model_spoof = model_from_json(loaded_model_json_spoof)
    model_spoof.load_weights(r"E:\antispoofing_model.h5")  # Replace with the actual path

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it
    obama_image = face_recognition.load_image_file("E:/tannu.jpg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [obama_face_encoding]
    known_face_names = ["tannu"]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    known_face_recognized = False
    unknown_face_detected_time = None

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Check if the frame is empty
        if not ret or frame is None:
            print("Error: Could not read frame from the webcam.")
            break

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    # Greet the recognized visitor by name
                    if not known_face_recognized:
                        if datetime.now().time().hour < 12:
                            greet_message = f"Good morning, {name}! Welcome back!"
                        elif 12 <= datetime.now().time().hour < 18:
                            greet_message = f"Good afternoon, {name}! Welcome back!"
                        else:
                            greet_message = f"Good evening, {name}! Welcome back!"

                        speak(greet_message)
                        known_face_recognized = True
                else:
                    # If face is unknown, get visitor's name and mobile number through voice input
                    name = "Unknown"
                    if unknown_face_detected_time is None:
                        unknown_face_detected_time = time.time()

                    if time.time() - unknown_face_detected_time > 5:  # Wait for 5 seconds before asking for info
                        visitor_name, visitor_mobile = get_visitor_info()

                        if visitor_name:
                            # Update the known faces with the new face information
                            known_face_encodings.append(face_encoding)
                            known_face_names.append(visitor_name)

                            speak(f"Thank you, {visitor_name}!")

                            # Convert image to bytes using OpenCV
                            _, buffer = cv2.imencode('.jpg', frame)
                            image_bytes = buffer.tobytes()

                            # Store visitor information with the binary image data in Firebase
                            ref = db.reference('/visitors2')
                            visitor_data = {
                                "name": visitor_name,
                                "mobile_number": visitor_mobile,
                                "photo": base64.b64encode(image_bytes).decode('utf-8'),  # Encode as base64 string
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            ref.push(visitor_data)

                        unknown_face_detected_time = None  # Reset the time tracking

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Text-to-speech command after face recognition loop completes
    if "Unknown" not in face_names and not known_face_recognized:
        speak("Thank you for visiting our restaurant!")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    # Start the Tkinter event loop
    root.mainloop()


# In[ ]:





# In[ ]:




