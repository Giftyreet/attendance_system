export default function TeacherDashboard() {
  return (
    <main className="min-h-screen p-10">
      <h1 className="text-4xl font-bold mb-10">
        Teacher Dashboard
      </h1>

      <div className="grid grid-cols-3 gap-6">

        <a
          href="/teacher/attendance"
          className="border p-6 rounded-lg"
        >
          Take Attendance
        </a>

        <a
          href="/teacher/history"
          className="border p-6 rounded-lg"
        >
          Attendance History
        </a>

        <div className="border p-6 rounded-lg">
          Low Attendance Students
        </div>

      </div>
    </main>
  );
}