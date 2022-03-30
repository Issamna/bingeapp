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
  return (
    <div className="user-tv-show-details">
      <Paper>
        <TableContainer>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Title</TableCell>
                <TableCell>Last Watched</TableCell>
                <TableCell>Times Watched</TableCell>
                <TableCell>Average Watch</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {props.userTvShows.map((row) => (
                <TableRow key={row.id}>
                  <TableCell component="th" scope="row">
                    {row.show_details.show_title}
                  </TableCell>
                  <TableCell component="th" scope="row">
                    {row.last_watched}
                  </TableCell>
                  <TableCell component="th" scope="row">
                    {row.times_watched}
                  </TableCell>
                  <TableCell component="th" scope="row">
                    {row.average_watch_length}
                  </TableCell>
                  <TableCell component="th" scope="row">
                    <button
                      className="btn-table"
                      onClick={() => props.onDeleteShow(row)}
                    >
                      Delete
                    </button>
                    <button
                      className="btn-table"
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
