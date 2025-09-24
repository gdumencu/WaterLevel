// frontend/src/pages/dashboard.tsx
import { useEffect, useState } from "react";
import jwt_decode from "jwt-decode";
import Sidebar from "../components/SideBar/ToggleButtons";
import PanelRenderer from "../components/Panels/PanelRenderer";
import useConfigLock from "../hooks/useConfigLock";
import LockBanner from "../components/LockBanner";

/**
 * JWT payload structure for WaterLevel authentication.
 * Ensure this matches the backend JWT claims.
 */
interface JwtPayload {
  userName: string; // or 'sub' if your backend uses that
  exp: number;
  role: string;
}
function fetchWithUser(url: string, options: any = {}) {
  const token = localStorage.getItem("token");
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "X-User": localStorage.getItem("userName") || "",
      Authorization: `Bearer ${token}`,
    },
  });
}

type PanelKey = "UARTConfig" | "JobConfig" | "Chart" | "RawData" | "AggregateData";

/**
 * Main dashboard page for WaterLevel telemetry system.
 * Displays user info, sidebar, and all panels available to the logged-in user.
 * Implements config lock logic.
 */
export default function Dashboard() {
  // Track logged-in user and role
  const [userName, setUser] = useState("");
  const [role, setRole] = useState("");

  // Track visibility of each panel (default: all visible)
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
      setUser(decoded.userName); // or decoded.sub if using 'sub'
      setRole(decoded.role.toLowerCase()); // normalize role
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

  // Use custom hook to track config lock status
  // Track config lock state
  const lockInfo = useConfigLock();

  useEffect(() => {
    const fetchLockStatus = async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/status`, {
        headers: { "X-User": userName },
      });
      const data = await res.json();
      console.log("Lock status:", data);
      lockInfo.setLockInfo(data);
    };

    fetchLockStatus();
    const interval = setInterval(fetchLockStatus, 5000);
    return () => clearInterval(interval);
  }, [userName]);

  // Lock/unlock handlers (call backend API)
  const handleLock = async () => {
    await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/lock`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userName, role }),
    });
  };

  const handleUnlock = async () => {
    await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/unlock`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userName, role }),
    });
  };


  // If dashboard is locked by another user, show banner and disable panels
  if (lockInfo.lockInfo.is_locked && lockInfo.lockInfo.locked_by !== userName) {
  return (
    <LockBanner
      locked_by={lockInfo.lockInfo.locked_by ?? "unknown"}
      role={lockInfo.lockInfo.role ?? "unknown"}
    />
  );
}


  return (
    <div className="dashboard-container">
      <div className="dashboard-topbar">
        <span className="dashboard-title">WaterLevel Dashboard</span>
        <span>
          <b>User:</b> {userName} <b>Role:</b> {role}
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
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
          {/* Pass lock state and handlers to panels */}
          <PanelRenderer
            role={role}
            visiblePanels={visiblePanels}
            user={userName}
            isLocked={lockInfo.lockInfo.is_locked}
            locked_by={lockInfo.lockInfo.locked_by}
            onLock={handleLock}
            onUnlock={handleUnlock}
          />
        </div>
      </div>
    </div>
  );
}
