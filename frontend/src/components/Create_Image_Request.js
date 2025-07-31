import React, { useState } from "react";

function Create_Image_Request() {
  const [requestType, setRequestType] = useState("");
  const [formData, setFormData] = useState({});
  const [error, setError] = useState("");

  const handleRequestTypeChange = (e) => {
    setRequestType(e.target.value);
    setFormData({});
    setError("");
  };

  const handleInputChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!requestType) {
      setError("Please select a request type.");
      return;
    }


    try {
      const res = await fetch("http://localhost:5000/api/create-image-request", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          request_type: requestType,
          ...formData,
        }),
      });

      if (res.ok) {
        alert("Request submitted successfully!");
        setRequestType("");
        setFormData({});
      } else {
        const text = await res.text();
        setError("Error: " + text);
      }
    } catch (err) {
      console.error(err);
      setError("Server error");
    }
  };

  const renderFormFields = () => {
    switch (requestType) {
      case "single":
        return (
          <>
            <input name="single image start date" placeholder="Enter Start Date" type="text" onChange={handleInputChange} required />
            <input name="single image end date" placeholder="Enter End Date" type="text" onChange={handleInputChange} required />
          </>
        );
      case "systematic":
        return (
          <>
            <input name="systematic image start date" placeholder="Enter Start Date" type="text" onChange={handleInputChange} required />
            <input name="systematic image end date" placeholder="Enter End Date" type="text" onChange={handleInputChange} required />
          </>
        );
      case "periodic":
        return (
          <>
            <input name="periodic image frequency" placeholder="Enter Frequency As Day" type="text" onChange={handleInputChange} required />
            <input name="number of consecutive days" placeholder="Consecutive Days Number" type="text" onChange={handleInputChange} required />
            <input name="periodic image start date" placeholder="Enter Start Date" type="text" onChange={handleInputChange} required />
            <input name="periodic image end date" placeholder="Enter End Date" type="text" onChange={handleInputChange} required />
          </>
        );
      case "recurring":
        return (
          <>
            <input name="recurring image outer loop duration" placeholder="Enter Outer Loop Duration" type="text" onChange={handleInputChange} required />
            <input name="inner loop duration per outer loop" placeholder="Inner's Duration Per Outer" type="text" onChange={handleInputChange} required />
            <input name="outer loop start date" placeholder="Start Date For Outer Loop" type="text" onChange={handleInputChange} required />
            <input name="outer loop end date" placeholder="End Date For Outer Loop" type="text" onChange={handleInputChange} required />
            <input name="inner loop start date" placeholder="Start Date For Inner Loop" type="text" onChange={handleInputChange} required />
            <input name="inner loop end date" placeholder="End Date For Inner Loop" type="text" onChange={handleInputChange} required />
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h2>Create Image Request</h2>
      <form onSubmit={handleSubmit}>
        <select value={requestType} onChange={handleRequestTypeChange} required>
          <option value="">-- Select Request Type --</option>
          <option value="single">Single Image</option>
          <option value="systematic">Systematic Image</option>
          <option value="periodic">Periodic Image</option>
          <option value="recurring">Recurring Image</option>
        </select>

        <div style={{ marginTop: "20px" }}>
          {renderFormFields()}
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" style={{ marginTop: "20px" }}>Submit</button>
      </form>
    </div>
  );
}

export default Create_Image_Request;