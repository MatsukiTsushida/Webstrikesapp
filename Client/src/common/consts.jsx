export const actions = {
  add: "add1",
  edit: "edit1",
  del: "del1",
};

export const functions = {
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
