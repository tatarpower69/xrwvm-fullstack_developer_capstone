import React from 'react';
import '../assets/bootstrap.min.css';
export default function Header() {
 const username = sessionStorage.getItem('username');
 async function logout(event) {
  event.preventDefault();
  const csrf = document.cookie.split('; ').find(x=>x.startsWith('csrftoken='))?.split('=')[1] || '';
  const response = await fetch('/djangoapp/logout',{method:'POST',headers:{'X-CSRFToken':csrf}});
  if (!response.ok) {alert('Logout failed');return;}
  sessionStorage.clear();
  alert('Logged out ' + username);
  window.location.href='/';
 }
 return <nav className="navbar navbar-expand navbar-light" style={{background:'darkturquoise',padding:24,gap:20}}><h2>Dealerships</h2><a href="/">Home</a><a href="/about/">About Us</a><a href="/contact/">Contact Us</a><span style={{marginLeft:'auto'}}>{username?<><strong>{username}</strong> <a href="/" onClick={logout}>Logout</a></>:<><a href="/login">Login</a> · <a href="/register">Register</a></>}</span></nav>;
}
