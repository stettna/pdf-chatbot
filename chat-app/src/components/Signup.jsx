import React, { useState } from "react";

export const Signup = (props) => {
        const [username, setUsername] = useState('');
        const [password1, setPassword1] = useState('');
        const [password2, setPassword2] = useState('');

        const handleSubmit = (event) => {
            event.preventDefault()

            const req = {username : username, password1 : password1, password2 : password2}

            fetch("http://localhost:3000/sign-up",
                  {method: "POST",
                  headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                  body: JSON.stringify(req)}
            )
            .then(
                response => response.json()
            )
            .then(
                data => {
                    if(data.status === 'success'){
                        props.onFormSwitch('upload')
                    }
                    else{
                        alert(data.message)
                    }
                }
            )
        }

        return (
            <div className= "auth-container">
                <h2>Sign-Up</h2>
                <form className="signup-form" onSubmit={handleSubmit}>
                    <label htmlFor="username">Username</label>
                    <input value={username} onChange={(event) => setUsername(event.target.value)} type="username" placeholder="Enter username" id= 'username' name='username'/>
                    <label htmlFor="password1">Password</label>
                    <input value={password1} onChange={(event) => setPassword1(event.target.value)} type="password" placeholder="Enter password" id='password1' name='password1'/>
                    <label htmlFor="password2">Confirm Password</label>
                    <input value={password2} onChange={(event) => setPassword2(event.target.value)} type="password" placeholder="Re-enter Password" id= 'password2' name='password2'/>
                    <button type="submit">Confirm</button>
                </form>
                <button className="link" onClick={() => props.onFormSwitch('login')}>Have an account? Login here!</button>
            </div>
        )
}