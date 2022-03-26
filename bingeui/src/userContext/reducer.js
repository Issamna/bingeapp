import { USER_CONTEXT_ACTIONS } from "./actionTypes";

const user = localStorage.getItem("user") ? localStorage.getItem("user") : "";
const accessToken = localStorage.getItem("accessToken")
  ? localStorage.getItem("accessToken")
  : "";

export const initialState = {
  isAuthenticated: user ? true : false,
  user: "" || user,
  loading: false,
  errorMessage: null,
};

export const UserContextReducer = (state, action) => {
  switch (action.type) {
    case USER_CONTEXT_ACTIONS.REQUEST_LOGIN:
      return {
        ...initialState,
        loading: true,
      };
    case USER_CONTEXT_ACTIONS.LOGIN_SUCCESS:
      localStorage.setItem("user", action.payload.user);
      localStorage.setItem("access_token", action.payload.access_token);
      return {
        ...initialState,
        isAuthenticated: true,
        user: action.payload.user,
        loading: false,
        errorMessage: null,
      };
    case USER_CONTEXT_ACTIONS.LOGIN_ERROR:
      return {
        ...initialState,
        loading: false,
        isAuthenticated: false,
        errorMessage: action.error,
      };
    case USER_CONTEXT_ACTIONS.LOGOUT:
      // Remove user & tokens from local storage
      localStorage.removeItem("user");
      localStorage.removeItem("access_token");
      return {
        ...initialState,
        isAuthenticated: false,
        user: "",
      };
    default:
      throw new Error(`Unhandled action type: ${action.type}`);
  }
};
