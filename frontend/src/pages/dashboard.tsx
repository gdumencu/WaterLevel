// frontend/src/pages/dashboard.tsx
import { useEffect, useState } from "react";
import jwt_decode from "jwt-decode"; // Correct default import

// Define the expected structure of the JWT payload
interface JwtPayload {
  sub: string; // subject (username)
  exp: number; // expiration timestamp (in seconds)
}

export default function Dashboard() {
  const [user, setUser] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    console.log("Token in localStorage:", token);

    if (!token) {
      console.warn("No token found, redirecting to login");
      window.location.href = "/login";
      return;
    }

    try {
      // Decode the token and assert its shape
      const decoded = jwt_decode<JwtPayload>(token.at.);
      

      // Check if the token has expired
      const now = Math.floor(Date.now() / 1000); // current time in seconds
      if (decoded.exp < now) {
        console.warn("Token expired, redirecting to login");
        localStorage.removeItem("token");
        window.location.href = "/login";
        return;
      }

      // Check if the token contains a valid subject
      if (!decoded.sub) {
        console.error("Invalid token: 'sub' field missing");
        throw new Error("Invalid token: 'sub' field missing");
      }

      // Set the user from the token
      setUser(decoded.sub);
    } catch (err) {
      console.error("Failed to decode token:", err);
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
  }, []);

  // Handle logout by clearing token and redirecting
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-topbar">
        <span className="dashboard-title">WaterLevel Dashboard</span>
        <span>
          <b>User:</b> {user}
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </span>
      </div>
      <div className="dashboard-body">
        <div className="sidebar">
          <button className="sidebar-btn">
            <img src="/icons/telemetry.svg" alt="Telemetry" />
          </button>
          <button className="sidebar-btn">
            <img src="/icons/settings.svg" alt="Settings" />
          </button>
        </div>
        <div className="dashboard-main">
          <div className="panel">
            <div className="panel-title">Welcome, {user}!</div>
            <div>
              {/* Add telemetry widgets, charts, or data here */}
              This is your WaterLevel dashboard. More features coming soon!
            </div>
          </div>
          <div className="dashboard-panels-bottom">
            <div className="raw-data-panel panel">
              <div className="panel-title">Raw Data</div>
              {/* Raw telemetry data goes here */}
            </div>
            <div className="aggregated-data-panel panel">
              <div className="panel-title">Aggregated Data</div>
              {/* Aggregated telemetry data goes here */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
