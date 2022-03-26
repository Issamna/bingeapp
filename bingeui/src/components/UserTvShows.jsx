import React, { useState, useEffect } from "react";
import client from "../utils/api-client";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

export default function UserTvShow(props) {
  const [searched, setSearched] = useState("");
  const [showData, setShowData] = useState([]);
  const [errorText, setErrorText] = useState(null);
  //console.log('load UserTvShow')

  return (
    <div className="user-tv-show-details">
      <h2>Your watched shows</h2>
      <Paper>
        <TableContainer>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Show</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {props.userTvShows.map((row) => (
                <TableRow key={row.id}>
                  <TableCell component="th" scope="row">
                    {row.show_details.show_title}
                  </TableCell>
                  <TableCell component="th" scope="row">
                    <button
                      className="btn btn-sm btn-outline-dark"
                      onClick={() => props.onDeleteShow(row)}
                    >
                      -
                    </button>
                  </TableCell>
                  <TableCell component="th" scope="row">
                    <button
                      className="btn btn-sm btn-outline-dark"
                      onClick={() => props.onShowViewHistory(row)}
                    >
                      History
                    </button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </div>
  );
}
// showdata id table --> usertvshow id showdata id lookin in usertvshow and grab that to delete it
