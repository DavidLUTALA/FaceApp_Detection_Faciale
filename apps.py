import cv2 as cv
import streamlit as st
import numpy as np
from PIL import Image
import os

# Configuration des modèles Haarcascade
FACE_CASCADE_PATH = 'haarcascade_frontalface_default.xml'
EYE_CASCADE_PATH = 'haarcascade_eye.xml'

# Chargement des classificateurs
face_cascade = cv.CascadeClassifier(FACE_CASCADE_PATH)
eye_cascade = cv.CascadeClassifier(EYE_CASCADE_PATH)

# Fonction pour détecter les visages
def detect_faces(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8)
    for (x, y, w, h) in faces:
        cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return image, faces

# Fonction pour détecter les yeux
def detect_eyes(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    for (x, y, w, h) in eyes:
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

# Fonction pour échanger les visages
def swap_faces(image, faces):
    if len(faces) != 2:
        st.error("L'image doit contenir exactement 2 visages pour effectuer un échange.")
        return image
    (x1, y1, w1, h1), (x2, y2, w2, h2) = faces
    face1 = image[y1:y1 + h1, x1:x1 + w1]
    face2 = image[y2:y2 + h2, x2:x2 + w2]
    face1_resized = cv.resize(face1, (w2, h2))
    face2_resized = cv.resize(face2, (w1, h1))
    image[y1:y1 + h1, x1:x1 + w1] = face2_resized
    image[y2:y2 + h2, x2:x2 + w2] = face1_resized
    return image

# Application principale avec Streamlit
def main():
    st.title("Détection et Manipulation de Visages")
    st.write("Téléchargez une image et choisissez une action.")

    # Debug : vérification de l'état
    st.write("### Étape : Interface chargée")
    
    uploaded_file = st.file_uploader("Téléchargez une image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.write("### Étape : Image téléchargée")  # Debug
        image = Image.open(uploaded_file)
        image = np.array(image)
        st.image(image, caption="Image d'origine", use_column_width=True)

        action = st.radio(
            "Choisissez une action :",
            ("Détecter les visages", "Détecter les yeux", "Échanger les visages")
        )

        if action == "Détecter les visages":
            st.write("### Étape : Détection des visages")  # Debug
            result_image, faces = detect_faces(image.copy())
            st.image(result_image, caption="Visages détectés", use_column_width=True)

        elif action == "Détecter les yeux":
            st.write("### Étape : Détection des yeux")  # Debug
            result_image = detect_eyes(image.copy())
            st.image(result_image, caption="Yeux détectés", use_column_width=True)

        elif action == "Échanger les visages":
            st.write("### Étape : Échange des visages")  # Debug
            _, faces = detect_faces(image.copy())
            if len(faces) >= 2:
                result_image = swap_faces(image.copy(), faces)
                st.image(result_image, caption="Visages échangés", use_column_width=True)
            else:
                st.error("Au moins 2 visages doivent être détectés pour effectuer un échange.")

if __name__ == "__main__":
    main()
