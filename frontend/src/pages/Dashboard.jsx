import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await api.get("/dashboard/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setDashboard(response.data);
      } catch (error) {
        console.error("Dashboard Error:", error);
      }
    };

    fetchDashboard();
  }, []);

  if (!dashboard) {
    return <h2>Loading Dashboard...</h2>;
  }

  return (
    <div style={{ padding: "30px" }}>
      <h1>EduFlow AI Dashboard</h1>

      {/* Dashboard Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <div
          style={{
            background: "#2563eb",
            color: "white",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center",
          }}
        >
          <h3>Total Applications</h3>
          <h1>{dashboard.applications.total}</h1>
        </div>

        <div
          style={{
            background: "#16a34a",
            color: "white",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center",
          }}
        >
          <h3>Approved</h3>
          <h1>{dashboard.applications.approved}</h1>
        </div>

        <div
          style={{
            background: "#dc2626",
            color: "white",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center",
          }}
        >
          <h3>Rejected</h3>
          <h1>{dashboard.applications.rejected}</h1>
        </div>

        <div
          style={{
            background: "#f59e0b",
            color: "white",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center",
          }}
        >
          <h3>Pending</h3>
          <h1>{dashboard.applications.pending}</h1>
        </div>
      </div>

      {/* Button */}
      <div style={{ marginTop: "30px", marginBottom: "30px" }}>
        <Link to="/applications">
          <button
            style={{
              padding: "12px 20px",
              background: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
            }}
          >
            View Applications
          </button>
        </Link>
      </div>

      <hr />

      {/* Risk Distribution */}
      <h2>Risk Distribution</h2>

      <p>🟢 Low Risk: {dashboard.risk_distribution.low}</p>
      <p>🟡 Medium Risk: {dashboard.risk_distribution.medium}</p>
      <p>🔴 High Risk: {dashboard.risk_distribution.high}</p>

      <hr />

      {/* AI Metrics */}
      <h2>AI Metrics</h2>

      <p>
        Average Eligibility Score:{" "}
        {dashboard.ai_metrics.average_eligibility_score}
      </p>

      <p>
        Average AI Confidence:{" "}
        {dashboard.ai_metrics.average_ai_confidence}
      </p>
    </div>
  );
}

export default Dashboard;