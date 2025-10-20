/**
 * AuditLogPanel.test.tsx
 * Unit tests for AuditLogPanel component (Task T8 - Audit Logging Lock/Unlock)
 */

import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import AuditLogPanel from "../components/Panels/AuditLogPanel";
import { beforeEach, describe } from "node:test";

// Mock fetch
declare const jest: any;
global.fetch = jest.fn();

const mockLogs = [
  {
    id: 1,
    action: "lock",
    role: "Admin",
    details: "Locked config panel",
    created_at: "2025-10-20T14:00:00Z",
  },
  {
    id: 2,
    action: "unlock",
    role: "Operator",
    details: "Unlocked config panel",
    created_at: "2025-10-20T15:00:00Z",
  },
];

describe("AuditLogPanel", () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
    localStorage.setItem("token", "mock-token");
  });

  it("renders loading state initially", async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockLogs,
    });

    render(<AuditLogPanel userName="Dorel" role="Admin" />);
    expect(screen.getByText(/Loading audit logs/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.queryByText(/Loading audit logs/i)).not.toBeInTheDocument();
    });
  });

  it("displays audit log entries", async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockLogs,
    });

    render(<AuditLogPanel userName="Dorel" role="Admin" />);

    await waitFor(() => {
      expect(screen.getByText("LOCK")).toBeInTheDocument();
      expect(screen.getByText("UNLOCK")).toBeInTheDocument();
      expect(screen.getByText("Admin")).toBeInTheDocument();
      expect(screen.getByText("Operator")).toBeInTheDocument();
    });
  });

  it("shows error and retry button on fetch failure", async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
    });

    render(<AuditLogPanel userName="Dorel" role="Admin" />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to fetch audit logs/i)).toBeInTheDocument();
      expect(screen.getByRole("button", { name: /Retry/i })).toBeInTheDocument();
    });
  });

  it("shows refresh button and triggers fetch on click", async () => {
    (fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => mockLogs,
    });

    render(<AuditLogPanel userName="Dorel" role="Admin" />);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: /Refresh Logs/i })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: /Refresh Logs/i }));
    expect(fetch).toHaveBeenCalledTimes(2); // initial + refresh
  });
});
``