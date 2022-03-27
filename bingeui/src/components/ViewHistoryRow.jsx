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

export default function ViewHistoryRow(props) {
  const setDateFromString = (dateString) => {
    return dateString ? new Date(dateString.replace(/-/g, "/")) : null;
  };

  const [viewHistory, setViewHistory] = useState(props.viewHistory);
  const [startDateSelected, setStartDateSelected] = useState(
    setDateFromString(props.viewHistory.start_date)
  );
  const [endDateSelected, setEndDateSelected] = useState(
    setDateFromString(props.viewHistory.end_date)
  );
  const [editSelected, setEditSelected] = useState(false);
  const [errorText, setErrorText] = useState(null);

  const handleCancel = () => {
    setStartDateSelected(setDateFromString(viewHistory.start_date));
    setEndDateSelected(setDateFromString(viewHistory.end_date));
    setEditSelected(false);
  };

  const handleUpdateViewHistory = async () => {
    if (endDateSelected !== null && startDateSelected > endDateSelected) {
      alert("End date can not be less than start date");
    } else {
      try {
        const response = await client(
          "/api/viewhistory/" + viewHistory.id + "/",
          {
            method: "PUT",
            data: {
              user_tvshow: viewHistory.user_tvshow,
              start_date: startDateSelected.toISOString().substring(0, 10),
              end_date:
                endDateSelected == null
                  ? endDateSelected
                  : endDateSelected.toISOString().substring(0, 10),
            },
          }
        );

        if (response.key && response.key.length > 0) {
          console.log("fail");
          console.log(response);
          setErrorText(response);
        } else {
          console.log(response);
          setViewHistory(response);
          setEditSelected(false);
        }
      } catch (error) {
        console.log(error);
        setErrorText(
          "Unable to fetch data from API. Make sure you're logged in!"
        );
      }
    }
  };

  return (
    <TableRow key={viewHistory.id}>
      <TableCell component="th" scope="row">
        {viewHistory.watch_length}
      </TableCell>
      <TableCell component="th" scope="row">
        {editSelected ? (
          <DatePicker
            defaultValue={startDateSelected}
            onChange={(value) => setStartDateSelected(value)}
            valueFormat={{ dateStyle: "medium" }}
          />
        ) : startDateSelected ? (
          startDateSelected.toLocaleDateString("en-us", {
            month: "short",
            day: "numeric",
            year: "numeric",
          })
        ) : null}
      </TableCell>
      <TableCell component="th" scope="row">
        {editSelected ? (
          <DatePicker
            defaultValue={endDateSelected}
            onChange={(value) => setEndDateSelected(value)}
            valueFormat={{ dateStyle: "medium" }}
          />
        ) : endDateSelected ? (
          endDateSelected.toLocaleDateString("en-us", {
            month: "short",
            day: "numeric",
            year: "numeric",
          })
        ) : null}
      </TableCell>
      <TableCell component="th" scope="row">
        {editSelected ? (
          <div>
            <button
              className="btn btn-sm btn-outline-dark"
              onClick={() => handleUpdateViewHistory()}
            >
              Save
            </button>
            <button
              className="btn btn-sm btn-outline-dark"
              onClick={() => handleCancel()}
            >
              Cancel
            </button>
          </div>
        ) : (
          <div>
            <button
              className="btn btn-sm btn-outline-dark"
              onClick={() => setEditSelected(true)}
            >
              Edit
            </button>
            <button
              className="btn btn-sm btn-outline-dark"
              onClick={() => props.onDeleteViewHistory(viewHistory)}
            >
              Delete
            </button>
          </div>
        )}
      </TableCell>
    </TableRow>
  );
}
