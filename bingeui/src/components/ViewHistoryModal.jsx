import React, { useState, useEffect } from "react";
import client from "../utils/api-client";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import "react-widgets/styles.css";
import DatePicker from "react-widgets/DatePicker";
import ViewHistoryRow from "./ViewHistoryRow";

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
    <div className="mmodal">
      <div className="modal-content">
        <div className="modal-header">
          <h3 className="modal-title">
            {props.userTvShow.show_details.show_title} View History
          </h3>
        </div>
        <div className="modal-body">
          <TableContainer>
            <Table aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Watch Length</TableCell>
                  <TableCell>Start Date</TableCell>
                  <TableCell>End Date</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell component="th" scope="row"></TableCell>
                  <TableCell component="th" scope="row">
                    <DatePicker
                      onChange={(value) => setStartDateSelected(value)}
                      valueFormat={{ dateStyle: "medium" }}
                    />
                  </TableCell>
                  <TableCell component="th" scope="row">
                    <DatePicker
                      valueFormat={{ dateStyle: "medium" }}
                      onChange={(value) => setEndDateSelected(value)}
                    />
                  </TableCell>
                  <TableCell component="th" scope="row">
                    <button
                      className="btn btn-sm btn-outline-dark"
                      onClick={() => handleAddViewHistory()}
                    >
                      Add
                    </button>
                  </TableCell>
                </TableRow>
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
        </div>
        <div className="modal-footer">
          <button
            className="btn btn-sm btn-outline-dark"
            onClick={props.onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
