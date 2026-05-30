import face_recognition
import pickle
import cv2


def recognize_faces(image_path,
                    embeddings_path="../embeddings/embeddings.pkl"):

    with open(embeddings_path, "rb") as f:
        data = pickle.load(f)

    known_embeddings = data["embeddings"]
    known_names = data["names"]

    image = cv2.imread(image_path)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)

    face_encodings = face_recognition.face_encodings(
        rgb,
        face_locations
    )

    recognized_students = []

    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(
            known_embeddings,
            face_encoding
        )

        name = "Unknown"

        if True in matches:

            matched_index = matches.index(True)

            name = known_names[matched_index]

        recognized_students.append(name)

    return recognized_students