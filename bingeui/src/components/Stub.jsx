import React, { useState, useEffect } from "react";
import client from "../utils/api-client";

const Stub = () => {
  const [stubData, setStubData] = useState(null);
  const [errorText, setErrorText] = useState(null);

  useEffect(async () => {
    const loadStubData = async () => {
      try {
        const response = await client("/stub/", {
          method: "GET",
        });
        if (!response) return;
        setStubData(response);
        setErrorText(null);
      } catch (error) {
        console.error(error);
        setStubData(null);
        setErrorText(
          "Unable to fetch data from /stub/. Make sure you're logged in!"
        );
      }
    };

    await loadStubData();
  }, []);

  return (
    <div data-testid="stubDataDisplay">
      <div className="card-header">
        <h1 className="display-1">Stub</h1>
      </div>
      <div className="card-body">
        <h2 className="display-6">
          Data from <code>/stub/</code> endpoint
        </h2>
        <p>
          The <code>/stub/</code> endpoint is protected by Authentication
          Tokens, meaning that a user must be logged in & have their
          authentication token present in the request header.
        </p>
        <p>
          The API client in <code>src/utils/api-client</code> will automatically
          detect if there's an access token in local storage, and attach it to
          any requests.
        </p>
        {errorText && (
          <div className="alert alert-danger" role="alert">
            {errorText}
          </div>
        )}
        <pre>{stubData && JSON.stringify(stubData, null, 2)}</pre>
        {console.log(stubData)}
      </div>
    </div>
  );
};

export default Stub;
