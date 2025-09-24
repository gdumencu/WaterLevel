//frontend\src\hooks\useConfigLock.ts
import { useEffect, useState } from "react";

/**
 * Custom hook to fetch and track config lock status from backend.
 */
export default function useConfigLock() {
  const [lockInfo, setLockInfo] = useState<{ is_locked: boolean; locked_by?: string; role?: string }>({ is_locked: false });
  const [userName, setUser] = useState("");
  useEffect(() => {
    // Fetch lock status from backend on mount and every 5 seconds
    const fetchLockStatus = async () => {
      try {
         const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/config/status`, {
        headers: { "X-User": userName },
      });
        const data = await res.json();
        setLockInfo(data);
      } catch (err) {
        setLockInfo({ is_locked: false });
      }
    };
    
    fetchLockStatus();
    const interval = setInterval(fetchLockStatus, 5000);
    return () => clearInterval(interval);
  }, []);

    return { lockInfo, setLockInfo };
}


