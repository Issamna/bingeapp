import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuthDispatch, USER_CONTEXT_ACTIONS } from "../../userContext";

export const PrivateLayout = ({ children, ...rest }) => {
  const dispatch = useAuthDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch({ type: USER_CONTEXT_ACTIONS.LOGOUT });
    navigate("/");
  };

  return (
    <div className="card">
      {children}
      <div className="card-footer text-muted">
        <button className="btn btn-sm btn-outline-dark" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default PrivateLayout;
