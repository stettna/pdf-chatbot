import React, { useState, useEffect } from "react";
import { Alert } from 'react'

export const Login = (props) => {
        const [username, setUsername] = useState('');
        const [password, setPassword] = useState('');

        const handleSubmit = (event) => {
            event.preventDefault()
            const req = {username : username, password : password}
            fetch("http://localhost:5000/login",
                  {method: "POST", headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                  body: JSON.stringify(req)}
            )
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success'){
                    props.onFormSwitch('upload')
                }
                else{
                    alert(data.message)
                }
            })
        }

        return (
            <div className="auth-container">
                <h2>Login</h2>
                <form className="login-form" onSubmit={handleSubmit}>
                    <label htmlFor="username">Username</label>
                    <input value={username} onChange={(event) => setUsername(event.target.value)} type="username" placeholder="Enter username" id= 'username' name='username'/>
                    <label htmlFor="password">Password</label>
                    <input value={password} onChange={(event) => setPassword(event.target.value)} type="password" placeholder="Enter password" id='password' name='password'/>
                    <button type="submit">Confirm</button>
                </form>
                <button className="link" onClick={() => props.onFormSwitch('signup')}>No account? Sign-up here!</button>
            </div>
        )
}