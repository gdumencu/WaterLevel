/**
 * AuditLogPanel.tsx
 * React component for displaying audit logs related to lock/unlock actions.
 *
 * ✅ Responsibilities:
 * - Fetch audit logs for the current user
 * - Display logs in a table format
 * - Show loading and error states
 * - Provide a manual refresh button
 */

import React, { useEffect, useState, useCallback } from "react";
import { format } from "date-fns";

// -----------------------------
// Type Definitions
// -----------------------------
interface AuditLogEntry {
  id: number;
  action: "lock" | "unlock";
  role: string;
  details?: string;
  created_at: string;
}

interface AuditLogPanelProps {
  userName: string;
  role: string;
}

// -----------------------------
// Component
// -----------------------------
export default function AuditLogPanel({ userName, role }: AuditLogPanelProps) {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // -----------------------------
  // Fetch logs function (reusable for retry/refresh)
  // -----------------------------
  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE}/audit/logs/me`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-User": userName,
          },
        }
      );
      if (!response.ok) {
        throw new Error("Failed to fetch audit logs");
      }
      const data = await response.json();
      setLogs(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [userName]);

  // -----------------------------
  // Initial fetch on mount
  // -----------------------------
  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  // -----------------------------
  // Render
  // -----------------------------
  return (
    <div className="panel audit-log-panel">
      <h2 className="panel-title">Audit Log</h2>

      {/* Refresh Button */}
      <div className="panel-controls">
        <button onClick={fetchLogs} className="refresh-button">
          🔄 Refresh Logs
        </button>
      </div>

      {/* Loading State */}
      {loading ? (
        <div className="panel-loading">Loading audit logs...</div>
      ) : error ? (
        <div className="panel-error">
          <p>{error}</p>
          <button onClick={fetchLogs} className="retry-button">
            🔁 Retry
          </button>
        </div>
      ) : logs.length === 0 ? (
        <div className="panel-empty">
          No audit log entries found for this user.
        </div>
      ) : (
        <table className="audit-log-table">
          <thead>
            <tr>
              <th>Action</th>
              <th>Role</th>
              <th>Details</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className={`audit-entry ${log.action}`}>
                <td>{log.action.toUpperCase()}</td>
                <td>{log.role}</td>
                <td>{log.details || "-"}</td>
                <td>{format(new Date(log.created_at), "yyyy-MM-dd HH:mm:ss")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
``