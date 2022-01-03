import React, { useState } from "react";
import Login from "./components/Login";
import Stub from "./components/Stub";

const App = () => {
  /*
  This is really bad authenticated state management, but just for demo purposes!

  The Stub component will re-attempt to fetch data from the backend whenever
  isLoggedIn changes (ie on successful login)

  use context api
  */
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div className="container">
      <Login onLogin={setIsLoggedIn} />
      <Stub isLoggedIn={isLoggedIn} />
    </div>
  );
};

export default App;