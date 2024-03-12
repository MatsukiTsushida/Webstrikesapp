import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { GridTable } from "./components/GridTable";

const App = () => {
  return (
    <div>
      <GridTable root="orders" />
      <GridTable root="users" />
    </div>
  );
};

const container = document.getElementById("root");
if (container != null) {
  const root = createRoot(container);
  root.render(React.createElement(App));
}
