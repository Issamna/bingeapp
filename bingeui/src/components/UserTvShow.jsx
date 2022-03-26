import React, { useState, useEffect } from "react";
import client from "../utils/api-client";

export default function UserTvShow(props) {
  const [showData, setShowData] = useState([]);
  const [errorText, setErrorText] = useState(null);
  console.log();
  useEffect(async () => {
    const loadShowData = async () => {
      try {
        const response = await client(
          "/api/tvshows/" + props.userTvShowDetail.show + "/",
          {
            method: "GET",
          }
        );
        if (!response) return;
        setShowData(response);
        setErrorText(null);
      } catch (error) {
        console.error(error);
        setShowData(null);
        setErrorText(
          "Unable to fetch data from API. Make sure you're logged in!"
        );
      }
    };

    await loadShowData();
  }, []);

  return (
    <div className="user-tv-show-details">
      {showData && (
        <div>
          <h3 className="show-title">{showData.show_title}</h3>
          <p>
            Last Watched:
            {props.userTvShowDetail.last_watched
              ? props.userTvShowDetail.last_watched
              : "Not watched"}
          </p>
        </div>
      )}
    </div>
  );
}
