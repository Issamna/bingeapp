import React, { useState, useEffect } from "react";
import client from "../utils/api-client";
import DropdownList from "react-widgets/DropdownList";
import "react-widgets/styles.css";

export default function ViewHistoryModal(props) {
  const [userTvShow, setUserTvShow] = useState(null);

  if (!props.view) {
    return null;
  }

  return (
    <div className="mmodal">
      <div className="modal-content">
        <div className="modal-header">
          <h3 className="modal-title">View History</h3>
        </div>
        <div className="modal-body">
            <h6>{props.userTvShow.id}</h6>
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
