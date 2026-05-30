from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from datetime import date
import shutil
import os

from db import (
    get_db,
    students_collection,
    teachers_collection,
    attendance_collection
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Attendance backend running"}


@app.get("/health/db")
def health_db():
    db = get_db()
    db.command("ping")
    return {"message": "MongoDB connected"}

@app.post("/register-student")
async def register_student(
    roll_no: str = Form(...),
    name: str = Form(...),
    section: str = Form(...),
    video: UploadFile = File(...)
):
    folder = f"dataset/{section}/{roll_no}"
    os.makedirs(folder, exist_ok=True)

    video_path = os.path.join(folder, f"{roll_no}.mp4")

    with open(video_path, "wb") as buffer:
        buffer.write(await video.read())

    from scripts.extract_frames import extract_frames
    result = extract_frames(video_path)

    students_collection.insert_one({
        "roll_no": roll_no,
        "name": name,
        "section": section,
        "video_uploaded": True
    })

    from scripts.create_embeddings import create_embeddings

    dataset_path = f"./dataset/{section}"
    embeddings_path = f"./embeddings/{section}_embeddings.pkl"

    embedding_result = create_embeddings(
        dataset_path=dataset_path,
        embeddings_path=embeddings_path
    )

    return {
        "message": "Student registered successfully",
        "frames_extracted": result,
        "embeddings_updated": embedding_result
    }


from typing import List
from fastapi import UploadFile, File, Form

@app.post("/recognize/{section}")
def recognize(
    section: str,
    teacher_id: str = Form(...),
    images: List[UploadFile] = File(...)
):
    from scripts.recognize import recognize_faces

    teacher = teachers_collection.find_one(
        {"teacher_id": teacher_id}
    )

    if not teacher:
        return {
            "error": "Teacher not found"
        }

    os.makedirs("./uploads", exist_ok=True)

    embeddings_path = f"./embeddings/{section}_embeddings.pkl"

    if not os.path.exists(embeddings_path):
        return {
            "error": f"No embeddings found for section {section}"
        }

    recognized_students = set()

    for image in images:

        image_path = f"./uploads/{image.filename}"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        students = recognize_faces(
            image_path,
            embeddings_path=embeddings_path
        )

        recognized_students.update(students)

    recognized_students = sorted(
        list(recognized_students)
    )

    all_students = list(
        students_collection.find(
            {"section": section}
        )
    )

    attendance_sheet = []

    for student in all_students:

        status = "A"

        if student["roll_no"] in recognized_students:
            status = "P"

        attendance_sheet.append({
            "roll_no": student["roll_no"],
            "name": student["name"],
            "status": status
        })

    attendance_document = {
        "teacher_id": teacher["teacher_id"],
        "teacher_name": teacher["name"],
        "subject": teacher["subject"],
        "section": section,
        "date": str(date.today()),
        "students": attendance_sheet
    }

    attendance_collection.insert_one(
        attendance_document
    )

    return {
        "message": "Attendance marked successfully",
        "teacher": teacher["name"],
        "subject": teacher["subject"],
        "section": section,
        "total_present": len(recognized_students),
        "attendance_sheet": attendance_sheet
    }

@app.post("/register-teacher")
async def register_teacher(
    teacher_id: str = Form(...),
    name: str = Form(...),
    subject: str = Form(...),
    section: str = Form(...)
):

    existing = teachers_collection.find_one(
        {"teacher_id": teacher_id}
    )

    if existing:
        return {
            "message": "Teacher already registered"
        }

    teachers_collection.insert_one({
        "teacher_id": teacher_id,
        "name": name,
        "assignments": [
            {
                "subject": subject,
                "section": section
            }
        ]
    })

    return {
        "message": "Teacher registered successfully"
    }