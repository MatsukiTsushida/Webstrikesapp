import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { AgGridReact } from "ag-grid-react"; // React Grid Logic
import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-quartz.css"; // Theme

const GridTable = ({ root }) => {
  const actions = {
    add: "add1",
    edit: "edit1",
    del: "del1",
  };

  const [rowData, setRowData] = useState([]);
  // Column Definitions: Defines & controls grid columns.
  const [colDefs, setColDefs] = useState([]);
  const [currentAction, setCurrentAction] = useState("");

  const fetching = async (root) => {
    const apiRes = await fetch(`http://127.0.0.1:5000/${root}`);
    const res = await apiRes.json();
    console.log(res.orders);
    setRowData(res.orders);
    setColDefs(Object.keys(res.orders[0]).map((x) => ({ field: x })));
  };
  useEffect(() => {
    fetching(root);
    return;
  }, []);

  const changeAction = (action) => {
    currentAction === action ? setCurrentAction("") : setCurrentAction(action);
    console.log(typeof actions[action]);
  };

  return (
    <div className="ag-theme-quartz" style={{ height: 500 }}>
      <AgGridReact rowData={rowData} columnDefs={colDefs} />
      <button onClick={() => changeAction(actions["add"])}>add</button>
      <button onClick={() => changeAction(actions["edit"])}>edit</button>
      <button onClick={() => changeAction(actions["del"])}>delete</button>
      <form>
        <button type="submit"></button>
        {(currentAction === actions["add"] ||
          currentAction === actions["edit"]) && (
          <input
            type="text"
            placeholder="User_id"
            id="user_id"
            name="user_id"
          />
        )}
        {(currentAction === actions["add"] ||
          currentAction === actions["edit"]) && (
          <input
            type="text"
            placeholder="Order_date"
            id="order_date"
            name="order_date"
          />
        )}
        {(currentAction === actions["del"] ||
          currentAction === actions["edit"]) && (
          <input type="text" placeholder="id" id="id" name="id" />
        )}
      </form>
    </div>
  );
};

const App = () => {
  return (
    <div>
      <GridTable root="orders" />
    </div>
  );
};

const container = document.getElementById("root");
const root = createRoot(container);
root.render(React.createElement(App));
