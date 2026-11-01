import React, {useState} from 'react';
import Header from '../Header/Header';

export default function Register() {
  const [error,setError] = useState('');
  async function register(event) {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.target));
    const response = await fetch('/djangoapp/register', {method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':document.cookie.split('; ').find(x=>x.startsWith('csrftoken='))?.split('=')[1] || ''}, body:JSON.stringify(data)});
    const result = await response.json();
    if (!response.ok) {setError(result.error || 'Registration failed'); return;}
    sessionStorage.setItem('username',result.userName);
    sessionStorage.setItem('firstname',data.firstName);
    sessionStorage.setItem('lastname',data.lastName);
    window.location.href='/dealers';
  }
  return <><Header/><main style={{maxWidth:500,margin:'40px auto'}}><h1>Create an account</h1><form onSubmit={register}>
    {['userName','firstName','lastName','email','password'].map(name=><label key={name} style={{display:'block',margin:16}}>{({userName:'Username',firstName:'First name',lastName:'Last name',email:'Email',password:'Password'})[name]}<input className="form-control" name={name} type={name==='password'?'password':name==='email'?'email':'text'} required minLength={name==='password'?10:1}/></label>)}
    <p role="alert">{error}</p><button className="btn btn-primary">Register</button></form></main></>;
}
