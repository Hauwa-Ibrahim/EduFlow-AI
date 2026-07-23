import { Link, Outlet, useNavigate } from "react-router-dom";
import {
  FaHome,
  FaFileAlt,
  FaUpload,
  FaBell,
  FaUser,
  FaSignOutAlt,
} from "react-icons/fa";

function MainLayout() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      {/* Sidebar */}
      <div
        style={{
          width: "250px",
          background: "#1f2937",
          color: "white",
          padding: "20px",
        }}
      >
        <h2 style={{ textAlign: "center" }}>EduFlow AI</h2>

        <hr />

        <p>
          <Link
            to="/dashboard"
            style={{
              color: "white",
              textDecoration: "none",
            }}
          >
            <FaHome /> Dashboard
          </Link>
        </p>

        <p>
          <Link
            to="/applications"
            style={{
              color: "white",
              textDecoration: "none",
            }}
          >
            <FaFileAlt /> Applications
          </Link>
        </p>

        <p>
          <Link
            to="/upload"
            style={{
              color: "white",
              textDecoration: "none",
            }}
          >
            <FaUpload /> Upload Documents
          </Link>
        </p>

        <p>
          <Link
            to="/notifications"
            style={{
              color: "white",
              textDecoration: "none",
            }}
          >
            <FaBell /> Notifications
          </Link>
        </p>

        <p>
          <Link
            to="/profile"
            style={{
              color: "white",
              textDecoration: "none",
            }}
          >
            <FaUser /> Profile
          </Link>
        </p>

        <br />

        <button
          onClick={logout}
          style={{
            width: "100%",
            padding: "10px",
            background: "#dc2626",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          <FaSignOutAlt /> Logout
        </button>
      </div>

      {/* Main Content */}
      <div
        style={{
          flex: 1,
          padding: "30px",
        }}
      >
        <Outlet />
      </div>
    </div>
  );
}

export default MainLayout;