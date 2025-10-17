// frontend/components/Panels/UARTConfig.tsx
import React, { useState } from "react";

/**
 * UART Config Panel - Only visible to Admin.
 * Implements config lock: disables dashboard for others when in config mode.
 */
export default function UARTConfig({ user, role, isLocked, locked_by, onLock, onUnlock }: {
  user: string;
  role: string;
  isLocked: boolean;
  locked_by?: string;
  onLock: () => void;
  onUnlock: () => void;
}) {
  const [configMode, setConfigMode] = useState(false);

  // Only Admin can see config buttons
  if (role !== "admin") return null;

  // If another user is locking, show message
  if (isLocked && locked_by !== user) {
    return (
      <div className="panel">
        <div className="panel-title">UART Config</div>
        <p>Dashboard unavailable: {locked_by} (admin) is configuring UART.</p>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-title">UART Config</div>
      <p>Admin-only UART configuration panel.</p>
      {!configMode ? (
        <button onClick={() => { onLock(); setConfigMode(true); }}>Config</button>
      ) : (
        <button onClick={() => { onUnlock(); setConfigMode(false); }}>Save Config</button>
      )}
      {/* Add UART config form fields here, only editable in configMode */}
      {configMode && <div>
        /* UART config fields go here */
        </div>
      }
    </div>
  );
}
