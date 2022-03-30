import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthDispatch, useAuthState, loginUser } from "../userContext";

const Login = () => {
  const authState = useAuthState();
  const dispatch = useAuthDispatch();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorText, setErrorText] = useState(null);

  useEffect(() => {
    if (authState.isAuthenticated) {
      navigateToDashBoard();
    }
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorText(null);
    try {
      const wasLoginSuccessful = await loginUser(dispatch, {
        email: email,
        password: password,
      });
      if (!wasLoginSuccessful) return;

      navigateToDashBoard();
    } catch (error) {
      console.error(error);
      alert("Error logging in!");
    }
  };

  const navigateToDashBoard = () => navigate("dashboard");

  return (
    <>
      <div>
        {errorText && (
          <div className="alert alert-danger" role="alert">
            {errorText}
          </div>
        )}
        <h1 className="login-title">Binge On</h1>
        <div className="login-box">
          <form noValidate onSubmit={handleLogin} data-testid="loginForm">
            <label>Email</label>
            <input
              type="text"
              name="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="email"
            />
            <label>Password</label>
            <input
              name="password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="password"
            />
            <input type="submit" value="LOGIN" />
          </form>
        </div>
      </div>
    </>
  );
};

export default Login;
