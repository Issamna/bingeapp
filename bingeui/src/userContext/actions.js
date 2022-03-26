import client from "../utils/api-client";
import { USER_CONTEXT_ACTIONS } from "./actionTypes";

export const loginUser = async (dispatch, loginData) => {
  try {
    dispatch({ type: USER_CONTEXT_ACTIONS.REQUEST_LOGIN });

    const response = await client("/auth/login/", {
      method: "POST",
      data: loginData,
    });

    if (response.key && response.key.length > 0) {
      dispatch({
        type: USER_CONTEXT_ACTIONS.LOGIN_SUCCESS,
        payload: {
          user: loginData.email,
          access_token: response.key,
        },
      });
      return true;
    }

    dispatch({
      type: USER_CONTEXT_ACTIONS.LOGIN_ERROR,
      error: "Access token not returned from backend!",
    });
    return false;
  } catch (error) {
    dispatch({ type: USER_CONTEXT_ACTIONS.LOGIN_ERROR, error });
    throw error;
  }
};
