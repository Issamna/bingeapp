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

export default function ViewHistoryRow(props) {
  const [viewHistory, setViewHistory] = useState(props.viewHistory);
  const [editSelected, setEditSelected] = useState(false);

  
  return (
    <TableRow key={viewHistory.id}>
      <TableCell component="th" scope="row">
        {viewHistory.watch_length}
      </TableCell>
      <TableCell component="th" scope="row">
        {viewHistory.start_date}
      </TableCell>
      <TableCell component="th" scope="row">
        {viewHistory.end_date}
      </TableCell>
      <TableCell component="th" scope="row">
        {editSelected ? 
          <div>
            <button className="btn btn-sm btn-outline-dark">Save</button>
            <button className="btn btn-sm btn-outline-dark">Cancel</button>
          </div> : 
          <div>
            <button className="btn btn-sm btn-outline-dark">Edit</button>
            <button className="btn btn-sm btn-outline-dark">Delete</button>
          </div>
        }
      </TableCell>
    </TableRow>
  );
}
