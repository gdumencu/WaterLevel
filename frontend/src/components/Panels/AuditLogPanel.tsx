import React, { useEffect, useState } from "react";
import { format } from "date-fns";

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

export default function AuditLogPanel({ userName, role }: AuditLogPanelProps) {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // useEffect(() => {
  //   const fetchLogs = async () => {
  //     try {
  //       const token = localStorage.getItem("token");
  //               const response = await fetch(
  //         //`${process.env.NEXT_PUBLIC_API_BASE}/api/audit/logs/me?start=2020-01-01T00:00:00Z&end=${new Date().toISOString()}`,
  //         `${process.env.NEXT_PUBLIC_API_BASE}/api/audit/logs/me`,
  //         {
  //           headers: {
  //             Authorization: `Bearer ${token}`,
  //             "X-User": userName,
  //           },
  //         }
  //       );
  //       if (!response.ok) {
  //         throw new Error("Failed to fetch audit logs");
  //       }
  //       const data = await response.json();
  //       setLogs(data);
  //     } catch (err: any) {
  //       setError(err.message);
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   fetchLogs();
  // }, [userName]);

  return (
    <div className="panel">
      <h2 className="panel-title">Audit Log</h2>

      {loading ? (
        <div className="panel-loading">Loading audit logs...</div>
      ) : error ? (
        <div className="panel-error">{error}</div>
      ) : logs.length === 0 ? (
        <div className="panel-empty">No audit log entries found for this user.</div>
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