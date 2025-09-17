// frontend/components/Panels/UARTConfig.tsx
import React from "react";

/**
 * UART Config Panel - Only visible to Admin
 */
export default function UARTConfig() {
  return (
    <div className="panel">
      <div className="panel-title">UART Config</div>
      <p>Admin-only UART configuration panel.</p>
    </div>
  );
}
