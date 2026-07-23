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
      const formData = new URLSearchParams();

      formData.append("grant_type", "password");
      formData.append("username", username);
      formData.append("password", password);
      formData.append("scope", "");
      formData.append("client_id", "");
      formData.append("client_secret", "");

      const response = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      console.log("Login Successful");
      console.log(response.data);

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      navigate("/dashboard");

    } catch (err) {
      console.log("Login Error:", err);
      console.log("Response:", err.response);
      console.log("Status:", err.response?.status);
      console.log("Data:", err.response?.data);

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
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <br />
        <br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <br />
        <br />

        <button type="submit">
          Login
        </button>
      </form>

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}
    </div>
  );
}

export default Login;