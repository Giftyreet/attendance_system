import face_recognition
import os
import pickle


def create_embeddings(dataset_path, embeddings_path):

    known_embeddings = []
    known_names = []

    for roll_no in os.listdir(dataset_path):

        student_folder = os.path.join(dataset_path, roll_no)

        if not os.path.isdir(student_folder):
            continue

        for image_name in os.listdir(student_folder):

            if not image_name.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):
                continue

            image_path = os.path.join(
                student_folder,
                image_name
            )

            image = face_recognition.load_image_file(
                image_path
            )

            face_encodings = face_recognition.face_encodings(
                image
            )

            if len(face_encodings) > 0:

                known_embeddings.append(
                    face_encodings[0]
                )

                known_names.append(
                    roll_no
                )

    data = {
        "embeddings": known_embeddings,
        "names": known_names
    }

    os.makedirs("./embeddings", exist_ok=True)

    with open(embeddings_path, "wb") as f:
        pickle.dump(data, f)

    return {
        "students_processed": len(set(known_names)),
        "total_embeddings": len(known_embeddings)
    }