import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // optional, create this too if you want styles

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);