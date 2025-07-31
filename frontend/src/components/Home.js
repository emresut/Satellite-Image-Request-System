import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>
        Image Request System
      </h1>
      <div style={styles.buttonContainer}>
        <button style={styles.button} onClick={() => navigate("/register")}>
          Register
        </button>
        <button style={styles.button} onClick={() => navigate("/login")}>
          Login
        </button>
        <button style={styles.button} onClick={() => navigate("/create-image-request")}>
          Create Image Request
        </button>
        <button style={styles.button} onClick={() => navigate("/all-image-requests")}>
          See All Image Requests
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    marginTop: "50px",
    fontFamily: "Arial, sans-serif",
  },
  title: {
    fontSize: "28px",
    marginBottom: "30px",
  },
  buttonContainer: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
    width: "250px",
    margin: "auto",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    borderRadius: "5px",
    border: "1px solid #555",
    cursor: "pointer",
    backgroundColor: "#f0f0f0",
  },
};

export default Home;