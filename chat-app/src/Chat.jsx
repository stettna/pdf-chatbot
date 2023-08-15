import React, { useState, useEffect } from "react";

export const Chat = (props) => {

        const [input, setInput] = useState('')
        const [output, setOutput]= useState('')

        const handleSubmit = (event) => {
            event.preventDefault()
            console.log(input)
        }

        return (
            <div className="auth-container">
                <h2>Chat Room</h2>
                <form className="login-form" onSubmit={handleSubmit}>
                    <input value={input} onChange={(event) => setInput(event.target.input)} type="username" placeholder="Enter question" id= 'input' name='input'/>
                    <button type="submit">Send</button>
                </form>
                <button onClick={() => props.onFormSwitch('Upload')}>End Chat</button>
            </div>
        )
}