// frontend/src/components/Panels/PanelRenderer.tsx
import React from "react";
import UARTConfig from "./UARTConfig";
import JobConfig from "./JobConfig";
import Chart from "./Chart";
import RawData from "./RawData";
import AggregateData from "./AggregateData";
import { JSX } from "react";

/**
 * PanelKey type: all possible panel keys for dashboard
 */
type PanelKey = "UARTConfig" | "JobConfig" | "Chart" | "RawData" | "AggregateData";

/**
 * Props for PanelRenderer: current role and visible panels
 */
interface PanelRendererProps {
  role: string;
  visiblePanels: Record<PanelKey, boolean>;
}

/**
 * PanelRenderer component: renders all panels available to the user,
 * stacking them vertically except Raw Data and Aggregate Data, which are side by side.
 */
export default function PanelRenderer({ role, visiblePanels }: PanelRendererProps) {
  // Panel definitions and allowed roles (use lowercase for roles)
  const panels: { key: PanelKey; component: JSX.Element; roles: string[] }[] = [
    { key: "UARTConfig", component: <UARTConfig />, roles: ["admin"] },
    { key: "JobConfig", component: <JobConfig />, roles: ["admin", "operator"] },
    { key: "Chart", component: <Chart />, roles: ["admin", "operator", "viewer"] },
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
          {showRaw && <div className="panel-col"><RawData /></div>}
          {showAggregate && <div className="panel-col"><AggregateData /></div>}
        </div>
      )}
    </div>
  );
}
