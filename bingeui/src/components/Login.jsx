import React, { useState } from "react";
import client from "../utils/api-client";

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorText, setErrorText] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorText(null);
    try {
      const response = await client("/auth/login/", {
        method: "POST",
        data: {
          email: email,
          password: password,
        },
      });
      if (!response) return;

      if (response.key && response.key.length > 0) {
        /* SET ACCESS TOKEN IN LOCAL STORAGE */
        localStorage.setItem("access_token", response.key);
        onLogin(true);
      }
    } catch (error) {
      console.error(error);
      setErrorText("Error logging in!");
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h2>
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
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="password"
            className="form-control"
          />
          <input type="submit" value="login" className="btn btn-primary" />
        </form>
      </div>
    </div>
  );
};

export default Login;