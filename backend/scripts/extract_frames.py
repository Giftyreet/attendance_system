import cv2
import face_recognition
import os


def extract_frames(video_path):

    student_folder = os.path.dirname(video_path)

    cap = cv2.VideoCapture(video_path)

    frame_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    step = 15
    saved_count = 0

    for frame_number in range(0, frame_total, step):

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(
            rgb,
            model="hog"
        )

        for top, right, bottom, left in faces:

            face = frame[top:bottom, left:right]

            filename = os.path.join(
                student_folder,
                f"face_{saved_count}.jpg"
            )

            cv2.imwrite(filename, face)

            saved_count += 1

    cap.release()

    os.remove(video_path)

    return {
        "faces_saved": saved_count
    }