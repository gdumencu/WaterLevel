// frontend/components/AuditLogTable.tsx

import React from "react";

interface AuditLog {
  id: number;
  user_id: number;
  action: string;
  role: string;
  created_at: string;
  details?: string;
}

interface Props {
  logs: AuditLog[];
  onSelect: (selectedIds: number[]) => void;
}

export default function AuditLogTable({ logs, onSelect }: Props) {
  const handleCheckboxChange = (id: number, checked: boolean) => {
    onSelect(
      checked
        ? [...new Set([...logs.map((log) => log.id), id])]
        : logs.filter((log) => log.id !== id).map((log) => log.id)
    );
  };

  return (
    <table className="audit-log-table">
      <thead>
        <tr>
          <th>Select</th>
          <th>Timestamp</th>
          <th>User ID</th>
          <th>Role</th>
          <th>Action</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        {logs.map((log) => (
          <tr key={log.id}>
            <td>
              <input
                type="checkbox"
                onChange={(e) => handleCheckboxChange(log.id, e.target.checked)}
                aria-label={`Select log entry ${log.id}`}
                title={`Select log entry ${log.id}`}
                />
            </td>
            <td>{new Date(log.created_at).toLocaleString()}</td>
            <td>{log.user_id}</td>
            <td>{log.role}</td>
            <td>{log.action}</td>
            <td>{log.details || "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}