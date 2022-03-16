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
    /* If our authState shows we're authenticated, navigate to stub instead of login form */
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
      setErrorText("Error logging in!");
    }
  };

  const navigateToDashBoard = () => navigate("dashboard");

  return (
    <>
      <div className="card-header">
        <h1 className="display-1">Login</h1>
      </div>
      <div className="card-body">
        <h2 className="display-6">
          Log in with <code>/auth/login/</code> endpoint
        </h2>
        <p>
          On successful login, the access token sent back from the server will
          be stored in local storage in your browser. This will allow access to
          protected endpoints, ie <code>/stub/</code>.
        </p>
        <p>
          To restart the process & force the user to login again, delete the
          local storage token in (for Chrome): <br />
          <code>
            Dev Tools &rarr; Application &rarr; Local Storage &rarr;
            http://localhost:3000/ &rarr; access_token
          </code>
          .
        </p>
        {errorText && (
          <div className="alert alert-danger" role="alert">
            {errorText}
          </div>
        )}

        <form
          noValidate
          onSubmit={handleLogin}
          className="form-group"
          data-testid="loginForm"
        >
          <input
            name="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="email"
            className="form-control"
          />
          <input
            name="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="password"
            className="form-control"
          />
          <input type="submit" value="login" className="btn btn-primary" />
        </form>
      </div>
    </>
  );
};

export default Login;