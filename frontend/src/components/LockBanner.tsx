import React from "react";

/**
 * Banner shown when dashboard is locked for configuration.
 */
export default function LockBanner({ locked_by, role }: { locked_by: string; role: string }) {
  return (
    <div className="lock-banner">
      <b>Dashboard unavailable:</b> {locked_by} ({role}) is configuring the application. Please wait until changes are saved.
    </div>
  );
}
