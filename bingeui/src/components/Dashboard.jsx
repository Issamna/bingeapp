import React, { useState, useEffect } from "react";
import client from "../utils/api-client";
import UserTvShow from "./UserTvShow";
import AddShowModal from "./AddShowModal";

const Dashboard = () => {
  const [userTvShowData, setUserTvShowData] = useState([]);
  const [errorText, setErrorText] = useState(null);
  const [viewShowModal, setViewTvShowModal] = useState(false)
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

  const userTvShows = userTvShowData.map((userTvShow) => (
    <UserTvShow key={userTvShow.id} userTvShowDetail={userTvShow} />
  ));
  

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
          <button className="btn btn-sm btn-outline-dark" onClick={() => setViewTvShowModal(true)}>
            Add New Show
          </button>
          <AddShowModal onClose={() => setViewTvShowModal(false)} view={viewShowModal} userTvShows={userTvShowData}/>
        </div>
        <div>{userTvShows}</div>
      </div>
    </div>
  );
};

export default Dashboard;
