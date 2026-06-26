"use client";

import { useState } from "react";
import { API_URL } from "@/lib/api";

export default function AttendancePage() {

  const [teacherId, setTeacherId] = useState("");

  const [assignments, setAssignments] = useState<any[]>([]);

  const [subject, setSubject] = useState("");

  const [section, setSection] = useState("");

  const [image, setImage] = useState<File | null>(null);

  const [attendance, setAttendance] = useState<any[]>([]);

  const [previewData, setPreviewData] = useState<any>(null);

  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);



  const loadAssignments = async () => {

    try {

      const response = await fetch(
        API_URL + `/teacher-assignments/${teacherId}`
      );

      const data = await response.json();

      setAssignments(data);

    } catch (err) {

      console.error(err);

    }

  };



  const handleAttendance = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {

    e.preventDefault();

    setLoading(true);

    try {

      const formData = new FormData();

      formData.append(
        "teacher_id",
        teacherId
      );

      formData.append(
        "subject",
        subject
      );

      formData.append(
        "section",
        section
      );

      if (image) {

        formData.append(
          "image",
          image
        );

      }

      const response = await fetch(

        API_URL + "/take-attendance",

        {
          method: "POST",
          body: formData
        }

      );

      const data = await response.json();

      setMessage(data.message);

      setAttendance(
        data.attendance_sheet || []
      );

      setPreviewData(data);

    } catch (err) {

      console.error(err);

    }

    setLoading(false);

  };



  const changeStatus = (

    index: number,

    value: string

  ) => {

    const updated = [...attendance];

    updated[index].status = value;

    setAttendance(updated);

  };



  const saveAttendance = async () => {

    if (!previewData) return;

    try {

      const response = await fetch(

        API_URL + "/save-attendance",

        {

          method: "POST",

          headers: {

            "Content-Type": "application/json"

          },

          body: JSON.stringify({

            teacher_id:
              previewData.teacher_id,

            teacher_name:
              previewData.teacher_name,

            subject:
              previewData.subject,

            section:
              previewData.section,

            date:
              previewData.date,

            attendance_sheet:
              attendance

          })

        }

      );

      const data = await response.json();

      alert(data.message);

      setAttendance([]);

      setPreviewData(null);

      setMessage("");

      setImage(null);

    }

    catch (err) {

      console.error(err);

    }

  };



  return (

    <main className="min-h-screen flex justify-center p-8">

      <div className="w-[700px] flex flex-col gap-4">

        <h1 className="text-4xl font-bold">

          Teacher Attendance

        </h1>

        <div className="flex gap-2">

          <input

            type="text"

            placeholder="Teacher ID"

            value={teacherId}

            onChange={(e) =>
              setTeacherId(e.target.value)
            }

            className="border p-2 rounded flex-1"

          />

          <button

            onClick={loadAssignments}

            className="bg-blue-600 text-white px-4 rounded"

          >

            Load

          </button>

        </div>

        <form

          onSubmit={handleAttendance}

          className="flex flex-col gap-4"

        >

          <select

            value={subject}

            onChange={(e) =>
              setSubject(e.target.value)
            }

            className="border p-2 rounded"

            required

          >

            <option value="">

              Select Subject

            </option>

            {assignments.map((item, index) => (

              <option

                key={index}

                value={item.subject}

              >

                {item.subject}

              </option>

            ))}

          </select>

          <select

            value={section}

            onChange={(e) =>
              setSection(e.target.value)
            }

            className="border p-2 rounded"

            required

          >

            <option value="">

              Select Section

            </option>

            {assignments.map((item, index) => (

              <option

                key={index}

                value={item.section}

              >

                {item.section}

              </option>

            ))}

          </select>

          <input

            type="file"

            accept="image/*"

            onChange={(e) =>

              setImage(

                e.target.files
                  ? e.target.files[0]
                  : null

              )

            }

            className="border p-2 rounded"

            required

          />

          <button

            type="submit"

            className="bg-green-600 text-white p-2 rounded"

          >

            {loading
              ? "Generating..."
              : "Generate Attendance"}

          </button>

        </form>

        {message && (

          <p className="text-blue-700">

            {message}

          </p>

        )}
                {attendance.length > 0 && (
          <>
            <table className="border border-collapse w-full mt-4">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border p-2">Roll No</th>
                  <th className="border p-2">Name</th>
                  <th className="border p-2">Status</th>
                </tr>
              </thead>

              <tbody>
                {attendance.map((student, index) => (
                  <tr key={student.roll_no}>
                    <td className="border p-2">
                      {student.roll_no}
                    </td>

                    <td className="border p-2">
                      {student.name}
                    </td>

                    <td className="border p-2">
                      <select
                        value={student.status}
                        onChange={(e) =>
                          changeStatus(
                            index,
                            e.target.value
                          )
                        }
                        className="border rounded p-1"
                      >
                        <option value="P">
                          Present
                        </option>

                        <option value="A">
                          Absent
                        </option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <button
              onClick={saveAttendance}
              className="bg-blue-600 text-white p-3 rounded mt-4"
            >
              Save Attendance
            </button>
          </>
        )}

      </div>
    </main>
  );
}