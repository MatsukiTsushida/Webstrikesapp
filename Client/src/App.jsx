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

  const functions = {
    [actions["add"]]: (props) => {
      fetch(`http://127.0.0.1:5000/orders`, {
        method: "POST",
        body: JSON.stringify(props),
      });
    },
    [actions["edit"]]: ({ id, user_id, order_date }) => {
      console.log(id);
      fetch(`http://127.0.0.1:5000/orders/${id}`, {
        method: "PUT",
        body: JSON.stringify({ user_id, order_date }),
      });
    },
    [actions["del"]]: ({ id }) => {
      fetch(`http://127.0.0.1:5000/orders/${id}`, {
        method: "DELETE",
      });
    },
  };

  const [rowData, setRowData] = useState([]);
  const [colDefs, setColDefs] = useState([]);
  // const [rowDefs, setRowDefs] = useState([]);
  // const [colData, setColData] = useState([]);
  const [currentAction, setCurrentAction] = useState("");

  const fetching = async (root) => {
    const apiRes = await fetch(`http://127.0.0.1:5000/${root}`);
    const res = await apiRes.json();
    // console.log(res.orders[0]["order_date"].slice(0, 16));
    console.log(res.orders);
    setRowData(res.orders);
    setColDefs(Object.keys(res.orders[0]).map((x) => ({ field: x })));
  };

  const Putzen = (a) => {
    // a.map((x) => x["order_date"].slice(0, 16));
    for (let i = 0; i <= a.length; i++) {
      a[i]["order_date"].slice(0, 16);
    }
  };
  // };
  // const fetching2 = async (root2) => {
  //   const apiRes = await fetch(`http://127.0.0.1:5000/${root}`);
  //   const res = await apiRes.json();
  //   console.log(res);
  //   setRowDefs(res.users);
  //   setColDefs(Object.keys(res.users[0]).map((x) => ({ field: x })));

  // };

  useEffect(() => {
    fetching(root);
    return;
  }, []);

  // useEffect(() => {
  //   fetching2(root2);
  //   return;
  // }, []);

  const changeAction = (action) => {
    currentAction === action ? setCurrentAction("") : setCurrentAction(action);
    console.log(typeof actions[action]);
  };

  return (
    <div className="ag-theme-quartz" style={{ height: 500 }}>
      <AgGridReact rowData={rowData} columnDefs={colDefs} />
      <AgGridReact rowData={rowDefs} columnDefs={colData} />
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

const App = () => {
  return (
    <div>
      <GridTable root="orders" />
      <GridTable root="users" />
    </div>
  );
};

const container = document.getElementById("root");
const root = createRoot(container);
root.render(React.createElement(App));
