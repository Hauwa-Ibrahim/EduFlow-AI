import { useEffect, useState } from "react";
import api from "../api/axios";

function Applications() {
  const [applications, setApplications] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await api.get("/applications/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setApplications(response.data);
      } catch (error) {
        console.error("Applications Error:", error);
      }
    };

    fetchApplications();
  }, []);

  const statusColor = (status) => {
    switch (status) {
      case "Approved":
        return "green";
      case "Rejected":
        return "red";
      case "Pending":
        return "orange";
      default:
        return "gray";
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Loan Applications</h1>

      <input
        type="text"
        placeholder="Search by Student ID or Loan Type..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{
          padding: "10px",
          width: "300px",
          marginTop: "20px",
          marginBottom: "20px",
          borderRadius: "8px",
          border: "1px solid #ccc",
        }}
      />

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "20px",
        }}
      >
        <thead
          style={{
            background: "#1f2937",
            color: "white",
          }}
        >
          <tr>
            <th style={{ padding: "12px" }}>ID</th>
            <th>Student ID</th>
            <th>Loan Type</th>
            <th>Academic Session</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Eligibility</th>
            <th>Risk</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {applications
            .filter(
              (app) =>
                app.student_id.toString().includes(search) ||
                app.loan_type
                  .toLowerCase()
                  .includes(search.toLowerCase())
            )
            .map((app) => (
              <tr
                key={app.id}
                style={{
                  textAlign: "center",
                  borderBottom: "1px solid #ddd",
                }}
              >
                <td style={{ padding: "12px" }}>{app.id}</td>
                <td>{app.student_id}</td>
                <td>{app.loan_type}</td>
                <td>{app.academic_session}</td>
                <td>₦{app.amount_requested}</td>

                <td>
                  <span
                    style={{
                      background: statusColor(app.status),
                      color: "white",
                      padding: "5px 10px",
                      borderRadius: "20px",
                    }}
                  >
                    {app.status}
                  </span>
                </td>

                <td>{app.eligibility_score}</td>

                <td>{app.risk_level}</td>

                <td>
                  <button
                    style={{
                      padding: "6px 12px",
                      background: "#2563eb",
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                    }}
                  >
                    👁 View
                  </button>
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}

export default Applications;