import React, {useState} from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Back_And_Logout_Button from "./components/Back_And_Logout_Button";
import Home from "./components/Home";
import Login from "./components/Login";
import Register from "./components/Register";
import Create_Image_Request from "./components/Create_Image_Request";
import All_Image_Requests from "./components/All_Image_Requests";

function App() {

   const [user, setUser] = useState(null);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Back_And_Logout_Button user={user} setUser={setUser} />}>
          <Route index element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login setUser={setUser} />} /> 
          <Route path="/create-image-request" element={<Create_Image_Request />} />
          <Route path="/all-image-requests" element={<All_Image_Requests />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
