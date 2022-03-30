import React from "react";
import { Link } from "react-router-dom";

export const PublicLayout = ({ children, ...rest }) => (
  <div className="card">
    {children}
    <div className="card-footer text-muted"></div>
  </div>
);

export default PublicLayout;
