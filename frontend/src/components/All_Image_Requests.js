import React, { useEffect, useState } from "react";

function All_Image_Requests() {
  const [requests, setRequests] = useState(null); // başlangıçta null
  const [error, setError] = useState(null);
  const [message, setMessage] = useState("");

  const displayOrder = [
    "request_code",
    "request_type",
    "status",
    "created_at",
    "single image start date",
    "single image end date",
    "systematic image start date",
    "systematic image end date",
    "periodic image start date",
    "periodic image end date",
    "periodic image frequency",
    "number of consecutive days",
    "recurring image outer loop duration",
    "inner loop duration per outer loop",
    "outer loop start date",
    "outer loop end date",
    "inner loop start date",
    "inner loop end date"
  ];

  useEffect(() => {
    fetch("http://localhost:5000/api/all-image-requests")
      .then((res) => {
        if (!res.ok) throw new Error("No request found");
        return res.json();
      })
      .then((data) => {
        setRequests(data.requests);
      })
      .catch((err) => setError(err.message));
  }, []);

  const handleDelete = (requestCode) => {
    if (!window.confirm(`Are you sure you want to delete request ${requestCode}?`)) return;

    fetch("http://localhost:5000/api/delete-image-request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ request_code: requestCode }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Delete failed");
        return res.json();
      })
      .then((data) => {
        setMessage(data.message || "Deleted");
        setRequests((prev) => prev.filter((req) => req.request_code !== requestCode));
      })
      .catch((err) => setError(err.message));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>All Image Requests</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}

      {requests === null ? (
        <p>...</p>
      ) : requests.length === 0 ? (
        <p>No image requests found.</p>
      ) : (
        <div>
          {requests.map((req) => (
            <div key={req.request_code} style={{ border: "1px solid #ccc", marginBottom: "10px", padding: "10px" }}>
              {displayOrder.map((key) =>
                req[key] !== undefined ? (
                  <p key={key}>
                    <strong>{key}:</strong> {req[key]}
                  </p>
                ) : null
              )}
              <button
                onClick={() => handleDelete(req.request_code)}
                style={{ backgroundColor: "red", color: "white", border: "none", padding: "5px 10px" }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default All_Image_Requests;