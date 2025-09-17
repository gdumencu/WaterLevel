// frontend/hooks/useRole.ts
import { useState, useEffect } from "react";
import jwt_decode from "jwt-decode";

export default function useRole() {
  const [role, setRole] = useState("");
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded: any = jwt_decode(token);
        setRole(decoded.role);
      } catch (err) {
        setRole("");
      }
    }
  }, []);
  return role;
}
