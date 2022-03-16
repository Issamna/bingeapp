import React from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { useAuthState } from "../userContext";
import PublicLayout from "./Layout/PublicLayout";
import PrivateLayout from "./Layout/PrivateLayout";
import Login from "./Login";
import Stub from "./Stub";
import Dashboard from "./Dashboard"

const PrivateRoute = ({ children }) => {
  const authState = useAuthState();
  if (!authState.isAuthenticated) {
    return <Navigate to="/" />;
  }

  return <PrivateLayout>{children}</PrivateLayout>;
};

const Router = () => (
  <BrowserRouter>
    <Routes>
      <Route
        path="/"
        element={
          <PublicLayout>
            <Login />
          </PublicLayout>
        }
      />
      <Route
        path="/stub"
        element={
          <PrivateRoute>
            <Stub />
          </PrivateRoute>
        }
      />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        }
      />
      <Route render={() => <h1>Page not found</h1>} />
    </Routes>
  </BrowserRouter>
);

export default Router;