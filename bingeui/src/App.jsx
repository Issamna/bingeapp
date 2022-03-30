import React from "react";
import Router from "./components/Router";
import AuthProvider from "./userContext/context";
import "./style.css";

const App = () => (
  <AuthProvider>
    <div>
      <Router />
    </div>
  </AuthProvider>
);

export default App;
