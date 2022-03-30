import React, { useState, useEffect } from "react";
import client from "../utils/api-client";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import DatePicker from "react-widgets/DatePicker";
import ViewHistoryRow from "./ViewHistoryRow";
import "react-widgets/styles.css";

export default function ViewHistoryModal(props) {
  const [viewHistories, setViewHistories] = useState(null);
  const [startDateSelected, setStartDateSelected] = useState(null);
  const [endDateSelected, setEndDateSelected] = useState(null);
  const [errorText, setErrorText] = useState(null);

  useEffect(async () => {
    const loadViewHistoryData = async () => {
      if (props.view) {
        try {
          const response = await client(
            "/api/utvshows/" + props.userTvShow.id + "/all_view_history/",
            {
              method: "GET",
            }
          );
          if (!response) return;
          setViewHistories(response);
          setErrorText(null);
        } catch (error) {
          console.error(error);
          setViewHistories(null);
          setErrorText(
            "Unable to fetch data from API. Make sure you're logged in!"
          );
        }
      }
    };

    await loadViewHistoryData();
  }, [props.userTvShow]);

  const handleAddViewHistory = async () => {
    if (endDateSelected !== null && startDateSelected > endDateSelected) {
      alert("End date can not be less than start date");
    } else {
      try {
        const response = await client("/api/viewhistory/", {
          method: "POST",
          data: {
            user_tvshow: props.userTvShow.id,
            start_date: startDateSelected.toISOString().substring(0, 10),
            end_date:
              endDateSelected == null
                ? endDateSelected
                : endDateSelected.toISOString().substring(0, 10),
          },
        });

        if (response.key && response.key.length > 0) {
          console.log("fail");
          console.log(response);
          setErrorText(response);
        } else {
          setViewHistories([response, ...viewHistories]);
        }
      } catch (error) {
        console.log(error);
        setErrorText(
          "Unable to fetch data from API. Make sure you're logged in!"
        );
      }
    }
  };

  const handleDeleteViewHistory = async (deleteViewHistory) => {
    try {
      const response = await client(
        "/api/viewhistory/" + deleteViewHistory.id + "/",
        {
          method: "DELETE",
        }
      );
      if (response.key && response.key.length > 0) {
        setErrorText(response);
      } else {
        setViewHistories((prevViewHistory) =>
          prevViewHistory.filter(
            (viewHistory) => viewHistory.id !== deleteViewHistory.id
          )
        );
      }
    } catch (error) {
      console.log(error);
      setErrorText(
        "Unable to fetch data from API. Make sure you're logged in!"
      );
    }
  };

  if (!props.view) {
    return null;
  }

  return (
    <div className="dashboard-modal">
      <div className="modal-view-history">
        <div className="modal-header">
          <h3 className="modal-title">
            {props.userTvShow.show_details.show_title} View History
          </h3>
        </div>
        <div className="modal-body-view-history">
          <div className="view-history-datepicker">
            <div className="view-history-datepicker-object">
              <DatePicker
                onChange={(value) => setStartDateSelected(value)}
                valueFormat={{ dateStyle: "medium" }}
              />
            </div>
            <div className="view-history-datepicker-object">
              <DatePicker
                valueFormat={{ dateStyle: "medium" }}
                onChange={(value) => setEndDateSelected(value)}
              />
            </div>
            <button className="btn-add" onClick={() => handleAddViewHistory()}>
              +
            </button>
          </div>
          <div className="dashboard-div">
            <div className="dashboard-table">
              <Paper>
                <TableContainer sx={{ maxHeight: 500 }}>
                  <Table aria-label="simple table">
                    <TableHead>
                      <TableRow>
                        <TableCell>Watch Length</TableCell>
                        <TableCell>Start Date</TableCell>
                        <TableCell>End Date</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {viewHistories &&
                        viewHistories.map((row) => (
                          <ViewHistoryRow
                            key={row.id}
                            viewHistory={row}
                            onDeleteViewHistory={(viewHistory) =>
                              handleDeleteViewHistory(viewHistory)
                            }
                          />
                        ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </div>
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn-can" onClick={props.onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
