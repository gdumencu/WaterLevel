// frontend/src/hooks/useConfigLock.ts

/**
 * 🔐 useConfigLock Hook for WaterLevel
 *
 * ✅ Responsibilities:
 * - Poll backend for config lock status
 * - Track lock state, locker identity, and role
 * - Provide lock/unlock actions with proper headers
 */

import { useEffect, useState } from "react";

/**
 * LockInfo type: represents the lock state returned by backend
 */
interface LockInfo {
  is_locked: boolean;
  locked_by?: string;
  role?: string;
  timestamp?: string;
}

/**
 * Custom hook to fetch and track config lock status from backend.
 */
export default function useConfigLock() {
  // -------------------------------------------------------------------
  // 1️⃣ Local state: lock info and current user
  // -------------------------------------------------------------------
  const [lockInfo, setLockInfo] = useState<LockInfo>({ is_locked: false });
  const [userName, setUserName] = useState<string>("");
  const [role, setRole] = useState<string>("");

  // -------------------------------------------------------------------
  // 2️⃣ Effect: fetch lock status on mount and every 5 seconds
  // -------------------------------------------------------------------
  useEffect(() => {
    const storedUser = localStorage.getItem("userName") || "";
    const storedRole = localStorage.getItem("role") || "";
    setUserName(storedUser);
    setRole(storedRole);

    const fetchLockStatus = async () => {
      try {
        const token = localStorage.getItem("token");

        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/status`, {
          headers: {
            "Authorization": `Bearer ${token}`,
            "X-User": storedUser,
          },
        });

        if (!res.ok) {
          throw new Error("Failed to fetch lock status");
        }

        const data = await res.json();
        setLockInfo(data);
      } catch (err) {
        console.error("Lock status fetch error:", err);
        setLockInfo({ is_locked: false });
      }
    };

    // Initial fetch
    fetchLockStatus();

    // Poll every 5 seconds
    const interval = setInterval(fetchLockStatus, 5000);

    // Cleanup on unmount
    return () => clearInterval(interval);
  }, []);

  // -------------------------------------------------------------------
  // 3️⃣ Lock action
  // -------------------------------------------------------------------
  const lockConfig = async () => {
    try {
      const token = localStorage.getItem("token");
      console.log("Locking config with user:", userName, "and role:", role);

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/lock`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ userName, role }),
      });

      if (!res.ok) {
        throw new Error("Failed to lock config");
      }

      const data = await res.json();
      setLockInfo({
        is_locked: true,
        locked_by: data.locked_by,
        role: data.role,
        timestamp: data.timestamp,
      });
    } catch (err) {
      console.error("Lock error:", err);
    }
  };

  // -------------------------------------------------------------------
  // 4️⃣ Unlock action
  // -------------------------------------------------------------------
  const unlockConfig = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/unlock`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ userName, role }),
      });

      if (!res.ok) {
        throw new Error("Failed to unlock config");
      }

      setLockInfo({ is_locked: false });
    } catch (err) {
      console.error("Unlock error:", err);
    }
  };

  // -------------------------------------------------------------------
  // 5️⃣ Return lock state and actions
  // -------------------------------------------------------------------
  return { lockInfo, setLockInfo, lockConfig, unlockConfig };
}