import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";

function ApplicationDetails() {
  const { id } = useParams();

  const [application, setApplication] = useState(null);

  useEffect(() => {
    const fetchApplication = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await api.get(`/applications/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setApplication(response.data);
      } catch (error) {
        console.error("Application Details Error:", error);
      }
    };

    fetchApplication();
  }, [id]);

  if (!application) {
    return (
      <div style={{ padding: "30px" }}>
        <h2>Loading Application...</h2>
      </div>
    );
  }

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "30px auto",
        padding: "30px",
        background: "#ffffff",
        borderRadius: "10px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      }}
    >
      <h1>Application #{application.id}</h1>

      <hr />

      <h2>Student Information</h2>

      <p>
        <strong>Name:</strong>{" "}
        {application.student
          ? `${application.student.first_name} ${application.student.last_name}`
          : "N/A"}
      </p>

      <p>
        <strong>Email:</strong>{" "}
        {application.student?.email || "N/A"}
      </p>

      <p>
        <strong>Institution:</strong>{" "}
        {application.student?.institution || "N/A"}
      </p>

      <p>
        <strong>Programme:</strong>{" "}
        {application.student?.programme || "N/A"}
      </p>

      <hr />

      <h2>Loan Information</h2>

      <p>
        <strong>Loan Type:</strong> {application.loan_type}
      </p>

      <p>
        <strong>Academic Session:</strong>{" "}
        {application.academic_session}
      </p>

      <p>
        <strong>Amount Requested:</strong> ₦
        {application.amount_requested.toLocaleString()}
      </p>

      <p>
        <strong>Status:</strong> {application.status}
      </p>

      <hr />

      <h2>AI Assessment</h2>

      <p>
        <strong>Eligibility Score:</strong>{" "}
        {application.eligibility_score}
      </p>

      <p>
        <strong>Recommendation:</strong>{" "}
        {application.recommendation}
      </p>

      <p>
        <strong>Risk Level:</strong>{" "}
        {application.risk_level}
      </p>

      <p>
        <strong>AI Confidence:</strong>{" "}
        {application.ai_confidence}%
      </p>

      <p>
        <strong>Verification Status:</strong>{" "}
        {application.verification_status}
      </p>

      <hr />

      <h2>Officer Review</h2>

      <p>
        <strong>Decision:</strong>{" "}
        {application.officer_review?.decision || "Not Reviewed"}
      </p>

      <p>
        <strong>Comment:</strong>{" "}
        {application.officer_review?.comment || "-"}
      </p>

      <p>
        <strong>Reviewed By:</strong>{" "}
        {application.officer_review?.reviewed_by || "-"}
      </p>

      <p>
        <strong>Reviewed At:</strong>{" "}
        {application.officer_review?.reviewed_at || "-"}
      </p>

      <hr />

      <h2>Uploaded Documents</h2>

      {application.documents.length === 0 ? (
        <p>No documents uploaded.</p>
      ) : (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: "15px",
          }}
        >
          <thead
            style={{
              background: "#1f2937",
              color: "white",
            }}
          >
            <tr>
              <th style={{ padding: "10px" }}>Document</th>
              <th>Status</th>
              <th>Confidence</th>
            </tr>
          </thead>

          <tbody>
            {application.documents.map((doc) => (
              <tr
                key={doc.id}
                style={{
                  textAlign: "center",
                  borderBottom: "1px solid #ddd",
                }}
              >
                <td style={{ padding: "10px" }}>
                  {doc.document_type}
                </td>

                <td>{doc.verification_status}</td>

                <td>
                  {doc.confidence_score !== null
                    ? `${doc.confidence_score}%`
                    : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ApplicationDetails;