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
    setViewHistorySelected(userTvShow)
    setViewHistoryModal(true);
  };

  const handleDeleteShow = async (deleteShow) => {
    try {

      const response = await client(
        "/api/utvshows/" + deleteShow.id + "/", 
        {
          method: "DELETE",
        }
      );
      console.log(response)
      if (response.key && response.key.length > 0) {
        console.log("fail");
        console.log(response);
        setErrorText(response);
      } else {
        setUserTvShowData(prevUserTvShow => prevUserTvShow.filter(userTvShow => userTvShow.id !== deleteShow.id));
      }
    } catch (error) {
      console.log(error);
      setErrorText(
        "Unable to fetch data from API. Make sure you're logged in!"
      );
    }
  };

  return (
    <div id="dashboardDisplay">
      <div className="card-header">
        <h1 className="display-1">Dashboard</h1>
      </div>
      <div className="card-body">
        {errorText && (
          <div className="alert alert-danger" role="alert">
            {errorText}
          </div>
        )}
      </div>
      <div>
        <div>
          <h2>Binge Next</h2>
          <button
            className="btn btn-sm btn-outline-dark"
            onClick={() => setViewTvShowModal(true)}
          >
            Add New Show
          </button>
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
        </div>
        <UserTvShows 
          userTvShows={userTvShowData} 
          onDeleteShow={(deleteShow) => handleDeleteShow(deleteShow)}
          onShowViewHistory={(userTvShow) => handleSetViewHistoryModal(userTvShow)}
        />
      </div>
    </div>
  );
};

export default Dashboard;
