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
    return <h2>Loading Application...</h2>;
  }

  return (
    <div style={{ padding: "30px" }}>
      <h1>Application #{application.id}</h1>

      <hr />

      <h2>Loan Information</h2>

      <p>
        <strong>Student ID:</strong> {application.student_id}
      </p>

      <p>
        <strong>Loan Type:</strong> {application.loan_type}
      </p>

      <p>
        <strong>Academic Session:</strong>{" "}
        {application.academic_session}
      </p>

      <p>
        <strong>Amount Requested:</strong> ₦
        {application.amount_requested}
      </p>

      <p>
        <strong>Status:</strong> {application.status}
      </p>

      <p>
        <strong>Eligibility Score:</strong>{" "}
        {application.eligibility_score}
      </p>

      <p>
        <strong>Risk Level:</strong> {application.risk_level}
      </p>
    </div>
  );
}

export default ApplicationDetails;