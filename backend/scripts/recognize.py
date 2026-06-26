import face_recognition
import pickle
import cv2
import os
import numpy as np


def recognize_faces(
    image_path,
    embeddings_path="../embeddings/embeddings.pkl"
):

    THRESHOLD = 0.65

    with open(embeddings_path, "rb") as f:
        data = pickle.load(f)

    known_embeddings = data["embeddings"]
    known_names = data["names"]

    image = cv2.imread(image_path)

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    face_locations = face_recognition.face_locations(
        rgb,
        model="cnn"
    )

    face_encodings = face_recognition.face_encodings(
        rgb,
        face_locations
    )

    recognized_students = []

    for (
        top,
        right,
        bottom,
        left
    ), face_encoding in zip(
        face_locations,
        face_encodings
    ):

        face_distances = face_recognition.face_distance(
            known_embeddings,
            face_encoding
        )

        best_match_index = np.argmin(
            face_distances
        )

        distance = face_distances[
            best_match_index
        ]

        if distance < THRESHOLD:

            name = known_names[
                best_match_index
            ]

            recognized_students.append(
                name
            )

        else:

            name = "Unknown"

        print(
            "Predicted:",
            name,
            "| Distance:",
            round(distance, 3)
        )

        color = (
            (0, 255, 0)
            if name != "Unknown"
            else (0, 0, 255)
        )

        cv2.rectangle(
            image,
            (left, top),
            (right, bottom),
            color,
            2
        )

        cv2.putText(
            image,
            str(name),
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    os.makedirs(
        "./uploads",
        exist_ok=True
    )

    cv2.imwrite(
        "./uploads/recognized_classroom.jpg",
        image
    )

    print(
        "Recognized Students:",
        sorted(set(recognized_students))
    )

    return list(
        set(recognized_students)
    )