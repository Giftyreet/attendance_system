"use client";

import { useState } from "react";
import { API_URL } from "@/lib/api";

export default function TeacherAssignments() {
  const [teacherId, setTeacherId] = useState("");
  const [subject, setSubject] = useState("");
  const [section, setSection] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    setLoading(true);
    setMessage("");

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

      const response = await fetch(
        API_URL + "/assign-teacher",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setMessage(data.message);

      if (
        data.message ===
        "Assignment added successfully"
      ) {
        setSubject("");
        setSection("");
      }
    } catch (error) {
      console.error(error);
      setMessage(
        "Unable to connect to backend"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex justify-center items-center">
      <form
        onSubmit={handleSubmit}
        className="w-[450px] border rounded-lg p-8 flex flex-col gap-4"
      >
        <h1 className="text-3xl font-bold text-center">
          Teacher Assignment
        </h1>

        <input
          type="text"
          placeholder="Teacher ID"
          value={teacherId}
          onChange={(e) =>
            setTeacherId(e.target.value)
          }
          className="border p-2 rounded"
          required
        />

        <input
          type="text"
          placeholder="Subject"
          value={subject}
          onChange={(e) =>
            setSubject(e.target.value)
          }
          className="border p-2 rounded"
          required
        />

        <input
          type="text"
          placeholder="Section"
          value={section}
          onChange={(e) =>
            setSection(e.target.value)
          }
          className="border p-2 rounded"
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white p-2 rounded"
        >
          {loading
            ? "Adding..."
            : "Add Assignment"}
        </button>

        {message && (
          <p className="text-center">
            {message}
          </p>
        )}
      </form>
    </main>
  );
}