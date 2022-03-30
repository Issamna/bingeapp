import React, { useContext, useReducer } from "react";
import { initialState, UserContextReducer } from "./reducer";

const UserContext = React.createContext();
const UserContextDispatch = React.createContext();

/* useContext method for getting the current Auth state */
export const useAuthState = () => useContext(UserContext);
/* useContext method for getting our useReducer dipatch*/
export const useAuthDispatch = () => useContext(UserContextDispatch);

const AuthProvider = ({ children }) => {
  const [user, dispatch] = useReducer(UserContextReducer, initialState);

  return (
    <UserContext.Provider value={user}>
      <UserContextDispatch.Provider value={dispatch}>
        {children}
      </UserContextDispatch.Provider>
    </UserContext.Provider>
  );
};

export default AuthProvider;
