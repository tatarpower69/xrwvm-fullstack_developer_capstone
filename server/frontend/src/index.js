import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

import { BrowserRouter } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById('root'));
async function start() {
  try {
    const response = await fetch('/djangoapp/session');
    if (!response.ok) throw new Error('Session lookup failed');
    const user = await response.json();
    if (user.userName) {
      sessionStorage.setItem('username', user.userName);
      sessionStorage.setItem('firstname', user.firstName);
      sessionStorage.setItem('lastname', user.lastName);
    } else {
      ['username','firstname','lastname'].forEach(key => sessionStorage.removeItem(key));
    }
  } catch (error) {
    root.render(<p role="alert">Unable to load your session. Please reload the page.</p>);
    return;
  }
  root.render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
);
}
start();
