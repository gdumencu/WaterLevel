import React, { useState } from 'react';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
//

/**frontend\src\pages\login.tsx
 * Login page component for WaterLevel.
 * Handles user authentication and displays errors.
 */
export default function Login() {
  // State for username, password, error, and loading
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle login button click
  const handleLogin = async () => {
    setError('');
    setLoading(true);
    try {
      // Send credentials to backend /login endpoint
      const res = await axios.post('http://localhost:8000/login', new URLSearchParams({
        username,
        password
      }));
      // Store JWT token in localStorage
      console.log('Login response:', res.data); 
      localStorage.setItem('token', res.data.access_token);
      setTimeout(() => {
          window.location.href = '/dashboard';
        }, 100); // small delay to ensure token is stored

      console.log('Token stored in localStorage');
      setLoading(false);
      console.log('Redirecting to dashboard...');
      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (err) {
      console.error("Login error:", err);
      setLoading(false);
      setError('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-title">WaterLevel Login</div>
        <form className="login-form" onSubmit={e => { e.preventDefault(); handleLogin(); }}>
          <label>
            Username
            <input
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              autoFocus
              required
            />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </label>
          <button className="login-button" type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
          {error && <div className="login-error">{error}</div>}
        </form>
      </div>
    </div>
  );
}
