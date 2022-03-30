import React, { useState, useEffect } from "react";
import client from "../utils/api-client";
import ViewHistoryModal from "./ViewHistoryModal";
import UserTvShows from "./UserTvShows";
import AddShowModal from "./AddShowModal";

const Dashboard = () => {
  const [userTvShowData, setUserTvShowData] = useState([]);
  const [errorText, setErrorText] = useState(null);
  const [viewShowModal, setViewTvShowModal] = useState(false);
  const [viewHistoryModal, setViewHistoryModal] = useState(false);
  const [viewHistorySelected, setViewHistorySelected] = useState(null);

  useEffect(async () => {
    const loadUserTvShowData = async () => {
      try {
        const response = await client("/api/utvshows/", {
          method: "GET",
        });
        if (!response) return;
        setUserTvShowData(response);
        setErrorText(null);
      } catch (error) {
        console.error(error);
        setUserTvShowData(null);
        setErrorText(
          "Unable to fetch data from API. Make sure you're logged in!"
        );
      }
    };

    await loadUserTvShowData();
  }, []);

  const handleAddShow = (newShow) => {
    setUserTvShowData([newShow, ...userTvShowData]);
    setViewTvShowModal(false);
  };

  const handleSetViewHistoryModal = (userTvShow) => {
    setViewHistorySelected(userTvShow);
    setViewHistoryModal(true);
  };

  const handleDeleteShow = async (deleteShow) => {
    try {
      const response = await client("/api/utvshows/" + deleteShow.id + "/", {
        method: "DELETE",
      });
      if (response.key && response.key.length > 0) {
        setErrorText(response);
      } else {
        setUserTvShowData((prevUserTvShow) =>
          prevUserTvShow.filter((userTvShow) => userTvShow.id !== deleteShow.id)
        );
      }
    } catch (error) {
      console.log(error);
      setErrorText(
        "Unable to fetch data from API. Make sure you're logged in!"
      );
    }
  };

  return (
    <div>
      <AddShowModal
        onClose={() => setViewTvShowModal(false)}
        onAddShow={(newShow) => handleAddShow(newShow)}
        view={viewShowModal}
        userTvShows={userTvShowData}
      />
      <ViewHistoryModal
        onClose={() => setViewHistoryModal(false)}
        view={viewHistoryModal}
        userTvShow={viewHistorySelected}
      />
      <div className="dashboard">
        <div className="">
          {errorText && (
            <div className="alert alert-danger" role="alert">
              {errorText}
            </div>
          )}
        </div>
        <div className="dashboard-div">
          <div className="dashboard-title">
            <h1>Your List</h1>
            <button
              className="btn-add"
              onClick={() => setViewTvShowModal(true)}
            >
              +
            </button>
          </div>
        </div>
        <div className="dashboard-div">
          <div className="dashboard-table">
            <UserTvShows
              userTvShows={userTvShowData}
              onDeleteShow={(deleteShow) => handleDeleteShow(deleteShow)}
              onShowViewHistory={(userTvShow) =>
                handleSetViewHistoryModal(userTvShow)
              }
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
