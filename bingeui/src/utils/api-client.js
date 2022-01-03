import * as fetch from "axios";

/*
API Client class that uses Axios to make requests to the Django backend
Usage examples:
- See src/components/Login for an example POST request w/ data
- See src/components/Stub for an example GET request
*/

const axios = fetch.create({
  baseURL: "http://127.0.0.1:8000/",
  headers: {
    "Content-Type": "application/json",
  },
});

const client = (
  endpoint,
  { method, data, headers: customHeaders, ...customConfig } = {}
) => {
  const accessToken = localStorage.getItem("access_token");
  const tokenHeader = {};
  if (accessToken) {
    tokenHeader["Authorization"] = `Token ${accessToken}`;
  }

  const config = {
    xsrfHeaderName: "X-CSRFToken",
    xsrfCookieName: "csrftoken",
    withCredentials: true,
    url: endpoint,
    method: method ? method : "get",
    data: data ?? undefined,
    headers: {
      ...tokenHeader,
      ...customHeaders,
    },
    ...customConfig,
  };

  return axios(config).then(async (response) => {
    if (response.status === 403) {
      return Promise.reject({ message: "Please re-authenticate" });
    }

    const { data } = await response;
    const isResponseOK = response.status >= 200 && response.status < 300;
    if (isResponseOK) {
      return data;
    } else {
      return Promise.reject(data);
    }
  });
};

export default client;