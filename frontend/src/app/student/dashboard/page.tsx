export default function StudentDashboard() {
  return (
    <main className="min-h-screen p-10">
      <h1 className="text-4xl font-bold mb-8">
        Student Dashboard
      </h1>

      <div className="border rounded-lg p-6 mb-8">
        <p>Name: Student Name</p>
        <p>Roll No: 23CS001</p>
        <p>Section: CSE-A</p>
      </div>

      <table className="w-full border">
        <thead>
          <tr>
            <th>Subject</th>
            <th>Professor</th>
            <th>Attendance %</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>DBMS</td>
            <td>Dr Sharma</td>
            <td>92%</td>
          </tr>
        </tbody>
      </table>
    </main>
  );
}