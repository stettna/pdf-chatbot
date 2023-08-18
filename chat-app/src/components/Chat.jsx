import React, { useState, useEffect } from "react";
import {ListBox} from "./ListBox"


/* {loading ? (<div className="spinner"></div> ): <></> } */

export const Chat = (props) => {

        const [inputArr, setInputArr] = useState([])

        const [input, setInput]= useState('')
        const [output, setOutput]= useState('')

        const [loading, setLoading] = useState(false);

        const handleSubmit = (event) => {
            event.preventDefault();
            setLoading(true)

            const req = {user_input : input}

            fetch("http://localhost:3000/chatroom",
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
                        setInputArr(prevArray => [...prevArray, "User: " + input, "AI: " + data.response]);
                        setInput('')
                    }
                    else{
                        alert(data.message)
                    }
                    setLoading(false)
                }
            )
        }

        return (
            <div className="auth-container">
                    <h2>Chat Room</h2>
                    <form className="login-form" onSubmit={handleSubmit}>
                        <textarea value={input} onChange={(event) => setInput(event.target.value)} placeholder="Enter question" id= 'input' name='input'/>
                        <button className="smallbtn" type="submit">Send</button>
                    </form>
                        <div className='ListBox'>
                            <ListBox input={inputArr}/>
                        </div>
                    <button className="smallbtn" onClick={() => props.onFormSwitch('upload')}>End Chat</button>
             </div>
       )
};