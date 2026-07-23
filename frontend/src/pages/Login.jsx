import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      console.log("========== LOGIN START ==========");
      console.log("Step 1: Preparing request");

      const formData = new URLSearchParams();

      formData.append("grant_type", "password");
      formData.append("username", username);
      formData.append("password", password);
      formData.append("scope", "");
      formData.append("client_id", "");
      formData.append("client_secret", "");

      console.log("Step 2: Sending request");

      const response = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      console.log("Step 3: Login successful");
      console.log(response.data);

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      console.log("Step 4: Token saved");
      console.log(
        localStorage.getItem("token")
      );

      console.log("Step 5: Navigating to dashboard");

      navigate("/dashboard");

      console.log("Step 6: Navigation completed");
      console.log("========== LOGIN END ==========");

    } catch (err) {
      console.error("========== LOGIN FAILED ==========");
      console.error("Full Error:", err);
      console.error("Response:", err.response);
      console.error("Status:", err.response?.status);
      console.error("Data:", err.response?.data);
      console.error("=================================");

      setError("Invalid email or password.");
    }
  };

  return (
    <div
      style={{
        maxWidth: "400px",
        margin: "100px auto",
      }}
    >
      <h1>EduFlow AI</h1>
      <h3>Student Loan Portal</h3>

      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
          required
        />

        <br />
        <br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
          required
        />

        <br />
        <br />

        <button type="submit">
          Login
        </button>
      </form>

      {error && (
        <p
          style={{
            color: "red",
            marginTop: "20px",
          }}
        >
          {error}
        </p>
      )}
    </div>
  );
}

export default Login;