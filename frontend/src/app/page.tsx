export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-8">
      <h1 className="text-5xl font-bold">
        Face Recognition Attendance System
      </h1>

      <div className="flex gap-6">
        <a
          href="/student/login"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg"
        >
          Student Portal
        </a>

        <a
          href="/teacher/login"
          className="bg-green-600 text-white px-6 py-3 rounded-lg"
        >
          Teacher Portal
        </a>
      </div>
    </main>
  );
}