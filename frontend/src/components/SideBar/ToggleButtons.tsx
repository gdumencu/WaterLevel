// frontend/src/components/SideBar/ToggleButtons.tsx
import React from "react";
import uartIcon from "../../assets/uart.png";
import jobIcon from "../../assets/job.png";
import chartIcon from "../../assets/chart.png";
import rawdataIcon from "../../assets/raw_data.png";
import aggregateIcon from "../../assets/aggregated.png";
import auditLogIcon from "../../assets/pdf.png";

type PanelKey = "UARTConfig" | "JobConfig" | "Chart" | "RawData" | "AggregateData" | "AuditLog";
const buttons: { key: PanelKey; label: string; icon: string | { src: string }; roles: string[] }[] = [
  { key: "UARTConfig", label: "UART Config", icon: uartIcon, roles: ["admin"] },
  { key: "JobConfig", label: "Job Config", icon: jobIcon, roles: ["admin", "operator"] },
  { key: "Chart", label: "Chart", icon: chartIcon, roles: ["admin", "operator", "viewer"] },
  { key: "RawData", label: "Raw Data", icon: rawdataIcon, roles: ["admin", "operator"] },
  { key: "AggregateData", label: "Aggregate Data", icon: aggregateIcon, roles: ["admin", "operator"] },
  { key: "AuditLog", label: "Audit Log", icon: auditLogIcon, roles: ["admin", "operator"] },
];

interface SidebarProps {
  role: string;
  visiblePanels: Record<PanelKey, boolean>;
  setVisiblePanels: React.Dispatch<React.SetStateAction<Record<PanelKey, boolean>>>;
}

export default function Sidebar({ role, visiblePanels, setVisiblePanels }: SidebarProps) {
  const handleToggle = (key: PanelKey) => {
    setVisiblePanels(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  return (
    <div className="sidebar">
      {buttons.map((btn) =>
        btn.roles.includes(role) ? (
          <button
            className={`sidebar-btn${visiblePanels[btn.key] ? " active" : ""}`}
            key={btn.key}
            onClick={() => handleToggle(btn.key)}
            title={`Show/hide ${btn.label}`}
          >
            <img src={typeof btn.icon === "string" ? btn.icon : btn.icon.src} alt={btn.label} />
            <span>{btn.label}</span>
          </button>
        ) : null
      )}
    </div>
  );
}
