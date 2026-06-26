"use client";

import { useState } from "react";

export default function RegisterStudent() {
  const [name, setName] = useState("");
  const [rollNo, setRollNo] = useState("");
  const [section, setSection] = useState("");
  const [video, setVideo] = useState<File | null>(null);

  const handleSubmit = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    if (!video) {
      alert("Please upload a video");
      return;
    }

    const formData = new FormData();

    formData.append("name", name);
    formData.append("roll_no", rollNo);
    formData.append("section", section);
    formData.append("video", video);

    try {
      const response = await fetch(
        "https://solid-space-bassoon-5g47gx7vx9q5fvgx7-8000.app.github.dev/register-student",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (response.ok) {
        alert(data.message);

        setName("");
        setRollNo("");
        setSection("");
        setVideo(null);
      } else {
        alert(data.message || "Registration failed");
      }
    } catch (error) {
      console.error(error);
      alert("Registration failed");
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center">
      <form
        onSubmit={handleSubmit}
        className="border p-6 rounded-lg w-[400px] space-y-4"
      >
        <h1 className="text-2xl font-bold">
          Student Registration
        </h1>

        <input
          type="text"
          placeholder="Name"
          className="border p-2 w-full"
          value={name}
          onChange={(e) =>
            setName(e.target.value)
          }
          required
        />

        <input
          type="text"
          placeholder="Roll Number"
          className="border p-2 w-full"
          value={rollNo}
          onChange={(e) =>
            setRollNo(e.target.value)
          }
          required
        />

        <input
          type="text"
          placeholder="Section"
          className="border p-2 w-full"
          value={section}
          onChange={(e) =>
            setSection(e.target.value)
          }
          required
        />

        <input
          type="file"
          accept="video/*"
          className="w-full"
          onChange={(e) => {
            const file = e.target.files?.[0];

            if (!file) return;

            if (file.size > 10 * 1024 * 1024) {
              alert("Video must be under 10 MB");
              e.target.value = "";
              return;
            }

            setVideo(file);
          }}
          required
        />

        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded w-full"
        >
          Register Student
        </button>
      </form>
    </div>
  );
}