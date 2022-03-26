import React from "react";
import Router from "./components/Router";
import AuthProvider from "./userContext/context";

const App = () => (
  <AuthProvider>
    <div className="container">
      <Router />
    </div>
  </AuthProvider>
);

export default App;
