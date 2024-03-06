import { functions, actions } from "../common/consts";
import { useState, useEffect } from "react";
import { AgGridReact } from "ag-grid-react"; // React Grid Logic
import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-quartz.css"; // Theme

export const GridTable = ({ root }) => {
  const [rowData, setRowData] = useState([]);
  const [colDefs, setColDefs] = useState([]);
  const [currentAction, setCurrentAction] = useState("");

  const fetching = async (root) => {
    const apiRes = await fetch(`http://127.0.0.1:5000/${root}`);
    const res = await apiRes.json();
    setRowData(res.data);
    setColDefs(Object.keys(res.data[0]).map((x) => ({ field: x })));
  };

  // const Putzen = (a) => {
  //   // a.map((x) => x["order_date"].slice(0, 16));
  //   for (let i = 0; i <= a.length; i++) {
  //     a[i]["order_date"].slice(0, 16);
  //   }
  // };
  // };

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
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const data = new FormData(e.target);
          const obj = {};
          for (let i of data) {
            obj[i[0]] = i[1];
          }
          console.log(obj);
          functions[currentAction](obj);
        }}
      >
        {(currentAction === actions["add"] ||
          currentAction === actions["edit"] ||
          currentAction === actions["del"]) && (
          <button type="submit">Submit</button>
        )}
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
