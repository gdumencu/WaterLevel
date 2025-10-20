// frontend/components/Panels/JobConfig.tsx
import React, { useState } from "react";

/**
 * Job Config Panel - Visible to Admin and Operator.
 * Implements config lock: disables dashboard for others when in config mode.
 */
export default function JobConfig({ user, role, isLocked, locked_by, onLock, onUnlock }: {
  user: string;
  role: string;
  isLocked: boolean;
  locked_by?: string;
  onLock: () => void;
  onUnlock: () => void;
}) {
  const [configMode, setConfigMode] = useState(false);

  // Only Admin/Operator can see config buttons
  if (role !== "admin" && role !== "operator") return null;

  // If another user is locking, show message
  if (isLocked && locked_by !== user) {
    return (
      <div className="panel">
        <div className="panel-title">Job Config</div>
        <p>Dashboard unavailable: {locked_by} ({role}) is configuring jobs.</p>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-title">Job Config</div>
      <p>Job configuration panel for Admin and Operator.</p>
      {!configMode ? (
        <button onClick={() => { onLock(); setConfigMode(true); }}>Config</button>
      ) : (
        <button onClick={() => { onUnlock(); setConfigMode(false); }}>Save Config</button>
      )}
      {/* Add job config form fields here, only editable in configMode */}
      {configMode && <div>/* Job config fields go here */</div>}
    </div>
  );
}

// function useState(arg0: boolean): [any, any] {
//   throw new Error("Function not implemented.");
// }

