// frontend/src/components/Panels/PanelRenderer.tsx
import React from "react";
import UARTConfig from "./UARTConfigPanel";
import JobConfig from "./JobConfigPanel";
import Chart from "./ChartPanel";
import RawData from "./RawDataPanel";
import AggregateData from "./AggregateData";
import AuditLogPanel from "./AuditLogPanel";
import { JSX } from "react";

/**
 * PanelKey type: all possible panel keys for dashboard
 */
type PanelKey = "UARTConfig" | "JobConfig" | "Chart" | "RawData" | "AggregateData" | "AuditLog";

/**
 * Props for PanelRenderer: current role, visible panels, user identity,
 * lock state, and lock/unlock handlers for config mode.
 */
interface PanelRendererProps {
  role: string;
  user: string;
  visiblePanels: Record<PanelKey, boolean>;
  isLocked: boolean;
  locked_by?: string;
  onLock: () => void;
  onUnlock: () => void;
}

/**
 * PanelRenderer component: renders all panels available to the user.
 * - Stacks most panels vertically.
 * - Renders Raw Data and Aggregate Data side by side.
 * - Passes lock state and handlers to config panels.
 */
export default function PanelRenderer({
  role,
  user,
  visiblePanels,
  isLocked,
  locked_by,
  onLock,
  onUnlock,
}: PanelRendererProps) {
  // Panel definitions and allowed roles (use lowercase for roles)
  const panels: { key: PanelKey; component: JSX.Element; roles: string[] }[] = [
    {
      key: "UARTConfig",
      component: (
        <UARTConfig
          user={user}
          role={role}
          isLocked={isLocked}
          locked_by={locked_by}
          onLock={onLock}
          onUnlock={onUnlock}
        />
      ),
      roles: ["admin"],
    },
    {
      key: "JobConfig",
      component: (
        <JobConfig
          user={user}
          role={role}
          isLocked={isLocked}
          locked_by={locked_by}
          onLock={onLock}
          onUnlock={onUnlock}
        />
      ),
      roles: ["admin", "operator"],
    },
    {
      key: "Chart",
      component: <Chart />,
      roles: ["admin", "operator", "viewer"],
    },
    {
      key: "AuditLog",
      component: <AuditLogPanel user={user} role={role} />,
      roles: ["admin", "operator"],
    },
  ];

  // Raw Data and Aggregate Data are rendered side by side
  const showRaw = ["admin", "operator"].includes(role) && visiblePanels["RawData"];
  const showAggregate = ["admin", "operator"].includes(role) && visiblePanels["AggregateData"];

  return (
    <div>
      {/* Stack all other panels vertically */}
      {panels.map(
        (panel) =>
          panel.roles.includes(role) &&
          visiblePanels[panel.key] && (
            <div key={panel.key} className="panel-stack">
              {panel.component}
            </div>
          )
      )}

      {/* Raw Data and Aggregate Data side by side */}
      {(showRaw || showAggregate) && (
        <div className="panel-row">
          {showRaw && (
            <div className="panel-col">
              <RawData/>
            </div>
          )}
          {showAggregate && (
            <div className="panel-col">
              <AggregateData />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
``