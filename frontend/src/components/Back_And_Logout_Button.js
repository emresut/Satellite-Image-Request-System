import React from "react";
import { useLocation, useNavigate, Outlet } from "react-router-dom";

function Back_And_Logout_Button({ user, setUser }) {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/logout", {
        method: "GET",
        credentials: "include",
      });

      if (res.ok) {
        setUser(null);
        navigate("/login");
      } else {
        alert("Logout failed.");
      }
    } catch (err) {
      console.error("Logout error:", err);
      alert("Logout error.");
    }
  };

  const showBackButton = location.pathname !== "/";
  const showLogout = user !== null;
  const showUsername = user !== null;

  return (
    <div>
      <header style={styles.header}>
        {showBackButton && (
          <button style={styles.button} onClick={() => navigate("/")}>
            Back
          </button>
        )}
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: "10px" }}>
          {showUsername && <span style={styles.username}>{user}</span>}
          {showLogout && (
            <button style={styles.logoutButton} onClick={handleLogout}>
              Logout
            </button>
          )}
        </div>
      </header>

      <main style={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}

const styles = {
  header: {
    padding: "10px 20px",
    backgroundColor: "#f1f1f1",
    borderBottom: "1px solid #ccc",
    display: "flex",
    alignItems: "center",
  },
  button: {
    padding: "8px 12px",
    fontSize: "14px",
    cursor: "pointer",
  },
  logoutButton: {
    padding: "8px 12px",
    fontSize: "14px",
    backgroundColor: "#dc3545",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  username: {
    fontWeight: "bold",
  },
  content: {
    padding: "20px",
  },
};

export default Back_And_Logout_Button;