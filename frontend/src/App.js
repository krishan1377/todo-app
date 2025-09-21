import React, { useEffect, useState } from "react";

function App() {
  const [todos, setTodos] = useState([]);
  const [task, setTask] = useState("");

  useEffect(() => {
    fetch("/api/todos")  // proxy to backend
      .then(res => res.json())
      .then(data => setTodos(data))
      .catch(err => console.error("Error fetching todos:", err));
  }, []);

  const addTodo = () => {
    fetch("/api/todos", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ task })
    })
    .then(res => res.json())
    .then(newTodo => {
      setTodos([...todos, [newTodo.id, newTodo.task]]);
      setTask("");
    });
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>✅ DevOps Todo App</h1>
      <input
        value={task}
        onChange={e => setTask(e.target.value)}
        placeholder="New task"
      />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map(todo => (
          <li key={todo[0]}>{todo[1]}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;