// frontend/src/pages/dashboard.tsx
import { useEffect, useState } from "react";
import jwt_decode from "jwt-decode";
import Sidebar from "../components/SideBar/ToggleButtons";
import PanelRenderer from "../components/Panels/PanelRenderer";

/**
 * JWT payload structure for WaterLevel authentication
 */
interface JwtPayload {
  sub: string;
  exp: number;
  role: string;
}
type PanelKey = "UARTConfig" | "JobConfig" | "Chart" | "RawData" | "AggregateData";

/**
 * Main dashboard page for WaterLevel telemetry system.
 * Displays user info, sidebar, and all panels available to the logged-in user.
 */
export default function Dashboard() {
  // Track logged-in user and role
  const [user, setUser] = useState("");
  const [role, setRole] = useState("");
  // Track visibility of each panel (default: all visible)
  // const [visiblePanels, setVisiblePanels] = useState<{
  //   UARTConfig: boolean;
  //   JobConfig: boolean;
  //   Chart: boolean;
  //   RawData: boolean;
  //   AggregateData: boolean;
  // }>({
  //   UARTConfig: true,
  //   JobConfig: true,
  //   Chart: true,
  //   RawData: true,
  //   AggregateData: true,
  // });
const [visiblePanels, setVisiblePanels] = useState<Record<PanelKey, boolean>>({
  UARTConfig: true,
  JobConfig: true,
  Chart: true,
  RawData: true,
  AggregateData: true,
});

  // Decode JWT and set user/role on mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/login";
      return;
    }
    try {
      const decoded = jwt_decode<JwtPayload>(token);
      setUser(decoded.sub);
      setRole(decoded.role); // keep lowercase for consistency
    } catch (err) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
  }, []);

  // Logout handler
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-topbar">
        <span className="dashboard-title">WaterLevel Dashboard</span>
        <span>
          <b>User:</b> {user} <b>Role:</b> {role}
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </span>
      </div>
      <div className="dashboard-body">
        {/* Sidebar with toggle buttons */}
        <Sidebar
          role={role}
          visiblePanels={visiblePanels}
          setVisiblePanels={setVisiblePanels}
        />
        {/* Main content area */}
        <div className="dashboard-main">
          <PanelRenderer role={role} visiblePanels={visiblePanels} />
        </div>
      </div>
    </div>
  );
}
