from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from datetime import date
import shutil
import os

from db import (
    get_db,
    students_collection,
    teachers_collection,
    attendance_collection, 
    teacher_assignments_collection,
    attendance_stats_collection
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://solid-space-bassoon-5g47gx7vx9q5fvgx7-3000.app.github.dev"
    ],
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

@app.get("/teacher-assignments/{teacher_id}")
async def get_teacher_assignments(
    teacher_id: str
):

    assignments = list(
        teacher_assignments_collection.find(
            {"teacher_id": teacher_id},
            {"_id": 0}
        )
    )

    return assignments

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
    subject: str = Form(...),
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
        "subject": subject,
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
        "subject": subject,
        "section": section,
        "total_present": len(recognized_students),
        "attendance_sheet": attendance_sheet
    }

@app.post("/register-teacher")
async def register_teacher(
    teacher_id: str = Form(...),
    name: str = Form(...)
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
        "name": name
    })

    return {
        "message": "Teacher registered successfully"
    }

@app.post("/assign-teacher")
async def assign_teacher(
    teacher_id: str = Form(...),
    subject: str = Form(...),
    section: str = Form(...)
):

    teacher = teachers_collection.find_one(
        {"teacher_id": teacher_id}
    )

    if not teacher:
        return {
            "message": "Teacher not found"
        }

    existing = teacher_assignments_collection.find_one(
        {
            "teacher_id": teacher_id,
            "subject": subject,
            "section": section
        }
    )

    if existing:
        return {
            "message": "Assignment already exists"
        }

    teacher_assignments_collection.insert_one({
        "teacher_id": teacher_id,
        "subject": subject,
        "section": section
    })

    return {
        "message": "Assignment added successfully"
    }

from scripts.recognize import recognize_faces

@app.post("/take-attendance")
async def take_attendance(
    teacher_id: str = Form(...),
    subject: str = Form(...),
    section: str = Form(...),
    image: UploadFile = File(...)
):

    teacher = teachers_collection.find_one(
        {"teacher_id": teacher_id}
    )

    if not teacher:
        return {
            "message": "Teacher not found"
        }

    os.makedirs("./uploads", exist_ok=True)

    image_path = f"./uploads/{image.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    embeddings_path = f"./embeddings/{section}_embeddings.pkl"

    if not os.path.exists(embeddings_path):
        return {
            "message": f"No embeddings found for section {section}"
        }

    recognized_students = recognize_faces(
        image_path,
        embeddings_path=embeddings_path
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

    # Preview only - nothing is saved to MongoDB
    return {
        "message": "Attendance generated successfully. Please review before saving.",
        "teacher_id": teacher["teacher_id"],
        "teacher_name": teacher["name"],
        "subject": subject,
        "section": section,
        "date": str(date.today()),
        "total_present": len(recognized_students),
        "attendance_sheet": attendance_sheet
    }

from pydantic import BaseModel
from typing import List


class AttendanceStudent(BaseModel):
    roll_no: str
    name: str
    status: str


class AttendanceSaveRequest(BaseModel):
    teacher_id: str
    teacher_name: str
    subject: str
    section: str
    date: str
    attendance_sheet: List[AttendanceStudent]

@app.post("/save-attendance")
async def save_attendance(request: AttendanceSaveRequest):

    attendance_document = {
        "teacher_id": request.teacher_id,
        "teacher_name": request.teacher_name,
        "subject": request.subject,
        "section": request.section,
        "date": request.date,
        "students": [
            student.model_dump()
            for student in request.attendance_sheet
        ]
    }

    # Save today's attendance
    attendance_collection.insert_one(attendance_document)

    # Update attendance statistics
    for student in request.attendance_sheet:

        existing_student = attendance_stats_collection.find_one(
            {
                "roll_no": student.roll_no,
                "section": request.section,
                "subject": request.subject
            }
        )

        # Create stats document if it doesn't exist
        if not existing_student:

            attendance_stats_collection.insert_one(
                {
                    "roll_no": student.roll_no,
                    "name": student.name,
                    "section": request.section,
                    "subject": request.subject,
                    "present": 0
                }
            )

        # Increment only if present
        if student.status == "P":

            attendance_stats_collection.update_one(
                {
                    "roll_no": student.roll_no,
                    "section": request.section,
                    "subject": request.subject
                },
                {
                    "$inc": {
                        "present": 1
                    }
                }
            )

    return {
        "message": "Attendance saved successfully"
    }

from fastapi.responses import FileResponse
from openpyxl import Workbook
import tempfile
@app.get("/download-attendance")
async def download_attendance(
    section: str,
    subject: str,
    date: str
):
    # Find the attendance for the selected day
    attendance = attendance_collection.find_one(
        {
            "section": section,
            "subject": subject,
            "date": date
        }
    )

    if not attendance:
        return {
            "message": "Attendance record not found."
        }

    # Total classes conducted till this date
    total_classes = attendance_collection.count_documents(
        {
            "section": section,
            "subject": subject,
            "date": {"$lte": date}
        }
    )

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    # Header
    ws.append([
        "Roll No",
        "Name",
        "Present Today",
        "Total Present",
        "Attendance %"
    ])

    for student in attendance["students"]:

        stats = attendance_stats_collection.find_one(
            {
                "roll_no": student["roll_no"],
                "section": section,
                "subject": subject
            }
        )

        total_present = stats["present"] if stats else 0

        percentage = (
            round((total_present / total_classes) * 100, 2)
            if total_classes > 0 else 0
        )

        ws.append([
            student["roll_no"],
            student["name"],
            student["status"],
            total_present,
            percentage
        ])

    # Temporary file
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".xlsx"
    )

    wb.save(temp_file.name)
    temp_file.close()

    filename = f"{section}_{subject}_{date}.xlsx"

    return FileResponse(
        path=temp_file.name,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )