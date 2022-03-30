import React, { useState, useEffect, useCallback } from "react";
import client from "../utils/api-client";
import DropdownList from "react-widgets/DropdownList";
import debounce from "lodash.debounce";
import "react-widgets/styles.css";

export default function UserTvShow(props) {
  const [showsData, setShowsData] = useState([]);
  const [searchShow, setSearchShow] = useState(null);
  const [errorText, setErrorText] = useState(null);
  const [showSelected, setShowSelected] = useState(null);
  const showsWatched = props.userTvShows.map((userTvShow) => {
    return userTvShow.show;
  });

  const findShowData = async (value) => {
    if (value.length > 4) {
      try {
        const response = await client(
          "/api/tvshows/search_tv_show/?search=" + value,
          {
            method: "GET",
          }
        );
        if (!response) return;
        setShowsData(response);
        setErrorText(null);
      } catch (error) {
        console.error(error);
        setShowsData(null);
        setErrorText(
          "Unable to fetch data from API. Make sure you're logged in!"
        );
      }
    }
  };

  const debouncedChangeHandler = useCallback(debounce(findShowData, 500), []);

  const handleAddShow = async () => {
    try {
      const response = await client("/api/utvshows/", {
        method: "POST",
        data: {
          show: showSelected.id,
        },
      });

      if (response.key && response.key.length > 0) {
        console.log("fail");
        console.log(response);
        setErrorText(response);
      } else {
        setShowSelected(null);
        props.onAddShow(response);
      }
    } catch (error) {
      console.log(error);
      setErrorText(
        "Unable to fetch data from API. Make sure you're logged in!"
      );
    }
  };

  function isShowWatched(show) {
    return showsWatched.includes(show.id);
  }

  if (!props.view) {
    return null;
  }

  return (
    <div className="dashboard-modal">
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">Add a show</h3>
        </div>
        <div className="modal-body">
          <DropdownList
            dataKey="id"
            defaultValue=""
            onSearch={(value) => findShowData(value)}
            onSelect={(value) => setShowSelected(value)}
            textField="show_title"
            filter="contains"
            data={showsData}
          />
        </div>
        <div>
          {showSelected && (
            <div className="modal-show-data">
              <h4>{showSelected.show_title}</h4>
              <button
                className={
                  !isShowWatched(showSelected) ? "btn-add" : "btn-disabled"
                }
                disabled={isShowWatched(showSelected)}
                onClick={() => handleAddShow()}
              >
                {!isShowWatched(showSelected) ? "+" : "Already in list"}
              </button>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn-can" onClick={props.onClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
