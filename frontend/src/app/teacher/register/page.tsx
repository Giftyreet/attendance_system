"use client";

import { API_URL } from "@/lib/api";
import { useState } from "react";

export default function TeacherRegister() {
  const [teacherId, setTeacherId] = useState("");
  const [name, setName] = useState("");
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

      formData.append("teacher_id", teacherId);
      formData.append("name", name);

      console.log(API_URL);

      const response = await fetch(API_URL + "/register-teacher", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setMessage(data.message);

      if (
        data.message ===
        "Teacher registered successfully"
      ) {
        setTeacherId("");
        setName("");
      }
    } catch (error) {
      console.error(error);
      setMessage("Unable to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex justify-center items-center">
      <form
        onSubmit={handleSubmit}
        className="w-[450px] rounded-lg border p-8 flex flex-col gap-4"
      >
        <h1 className="text-3xl font-bold text-center">
          Teacher Registration
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
          placeholder="Teacher Name"
          value={name}
          onChange={(e) =>
            setName(e.target.value)
          }
          className="border p-2 rounded"
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-green-600 text-white p-2 rounded"
        >
          {loading
            ? "Registering..."
            : "Register"}
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