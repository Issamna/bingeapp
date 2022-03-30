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
    <div>
      <nav>
        <div>
          <h1>Binge On</h1>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      {children}
    </div>
  );
};

export default PrivateLayout;
