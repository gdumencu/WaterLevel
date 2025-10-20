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
  userName: string;
  exp: number;
  role: string;
}

// ✅ Updated PanelKey type to include AuditLog
type PanelKey = "UARTConfig" | "JobConfig" | "Chart" | "RawData" | "AggregateData" | "AuditLog";

/**
 * Main dashboard page for WaterLevel telemetry system.
 * Displays user info, sidebar, and all panels available to the logged-in user.
 * Implements config lock logic.
 */
export default function Dashboard() {
  // -------------------------------------------------------------------
  // 1️⃣ Track logged-in user and role
  // -------------------------------------------------------------------
  const [userName, setUser] = useState("");
  const [role, setRole] = useState("");

  // -------------------------------------------------------------------
  // 2️⃣ Track visibility of each panel
  // -------------------------------------------------------------------
  const [visiblePanels, setVisiblePanels] = useState<Record<PanelKey, boolean>>({
    UARTConfig: true,
    JobConfig: true,
    Chart: true,
    RawData: true,
    AggregateData: true,
    AuditLog: true,
  });

  // -------------------------------------------------------------------
  // 3️⃣ Decode JWT and set user/role on mount
  // -------------------------------------------------------------------
  useEffect(() => {
    const token = localStorage.getItem("token");
    console.log("Decoding token on dashboard mount:", token);
    
    if (!token) {
      window.location.href = "/login";
      return;
    }
    try {
      const decoded = jwt_decode<JwtPayload>(token);
      setUser(decoded.userName);
      setRole(decoded.role.toLowerCase());
      localStorage.setItem("userName", decoded.userName);
      localStorage.setItem("role", decoded.role.toLowerCase());
    } catch (err) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
  }, []);

  // -------------------------------------------------------------------
  // 4️⃣ Logout handler
  // -------------------------------------------------------------------
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userName");
    localStorage.removeItem("role");
    window.location.href = "/login";
  };

  // -------------------------------------------------------------------
  // 5️⃣ Use custom hook to track config lock status
  // -------------------------------------------------------------------
  const lockInfo = useConfigLock();

  useEffect(() => {
    const fetchLockStatus = async () => {
      const token = localStorage.getItem("token");
      console.log("Fetching lock status for user:", userName);

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/status`, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "X-User": userName,
        },
      });

      const data = await res.json();
      console.log("Lock status:", data);
      lockInfo.setLockInfo(data);
    };

    fetchLockStatus();
    const interval = setInterval(fetchLockStatus, 50000);
    return () => clearInterval(interval);
  }, [userName]);

  // -------------------------------------------------------------------
  // 6️⃣ Lock/unlock handlers with proper headers
  // -------------------------------------------------------------------
  const handleLock = async () => {
    const token = localStorage.getItem("token");
    console.log("Locking config by", userName, "with role", role);

    await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/lock`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ userName, role }),
    });
  };

  const handleUnlock = async () => {
    const token = localStorage.getItem("token");
    console.log("Unlocking config by", userName, "with role", role);

    await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/unlock`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ userName, role }),
    });
  };

  // -------------------------------------------------------------------
  // 7️⃣ Show lock banner if dashboard is locked by another user
  // -------------------------------------------------------------------
  if (lockInfo.lockInfo.is_locked && lockInfo.lockInfo.locked_by !== userName) {
    return (
      <LockBanner
        locked_by={lockInfo.lockInfo.locked_by ?? "unknown"}
        role={lockInfo.lockInfo.role ?? "unknown"}
      />
    );
  }

  // -------------------------------------------------------------------
  // 8️⃣ Render dashboard layout
  // -------------------------------------------------------------------
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
``