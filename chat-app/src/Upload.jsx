import React, { useState, useEffect } from "react";

export const Upload = (props) => {

        const [file, setFile] = useState()
        const[isSelected, setIsSelected]= useState(false)

        const handleChange = (event) => {
                setFile(event.target.files[0]);
                setIsSelected(true);
        }

        const handleSubmit = (event) => {
            event.preventDefault()
            console.log(file)
        }

        return (
            <div className="auth-container">
                <h2>Upload PDF</h2>
                <form className="login-form" onSubmit={handleSubmit}>
                    <input value={file} onChange={(event) => setFile(event.target.value)} type="file" id= 'file' name='file'/>
                    <button type="submit">Submit</button>
                </form>
                <button onClick={() => props.onFormSwitch('start-chat')}>Chat</button>
            </div>
        )
}