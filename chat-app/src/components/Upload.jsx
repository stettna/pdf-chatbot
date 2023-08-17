import React, { useState, useEffect } from "react";
import {ListBox} from "./ListBox"

let filesArr = [];

export const Upload = (props) => {

        const [selectedFile, setSelectedFile] = useState()
        const [isSelected, setIsSelected]= useState(false)

        const [fileNames, setFileNames] = useState([])
        const [hasFileList, setHasFileList] = useState(false)

        const handleChange = (event) => {
                console.log('filename:'+event.target.files[0].name)
                setSelectedFile(event.target.files[0]);
                setIsSelected(true);
        }

        const handleSubmit = (event) => {
            event.preventDefault()

            const formData = new FormData()

            formData.append("file", selectedFile);

            fetch("http://localhost:3000/upload-file",
                  {method: "POST",
                  body: formData}
            ).then(response => response.json()).then(
                      data =>  {
                        if(data.status === 'success'){
                            console.log(fileNames)
                            setFileNames(prevArray => [...prevArray, selectedFile.name]);
                            console.log(fileNames)
                        }
                        else{
                            alert(data.message)
                        }
                     }
           )
        }

        const handleButton = (event, loc, page) => {
            fetch("http://localhost:3000/" + loc,
                  {method: "GET"}).then(
                  response => response.json()).then(
                      data =>  {
                        if(data.status === 'success'){
                            props.onFormSwitch(page)
                        }
                        else{
                            alert(data.message)
                        }
                        if(loc === 'clr-data'){
                            setFileNames([])
                        }
                     }
            )
        }

        function getFileNames(){
           fetch("http://localhost:3000/get-file-list",{method: "GET"} ).then(
                response => response.json()).then(
                      data =>  {
                        if(data.status === 'success'){
                           console.log(data)
                           setFileNames(data.files)
                           console.log(filesArr)
                        }
                        else{
                            alert(data.message)
                        }
                     }
           )
        }

        useEffect(() => {
            getFileNames()
            setFileNames(prevArray => [...prevArray]);
        }, []);


        return (
            <div className="auth-container">
                <h2>Upload PDF</h2>
                <form className="login-form" onSubmit={handleSubmit}>
                    <input  onChange={(event) => handleChange(event)} type="file" id= 'file' name='file'/>
                    <button type="submit">Submit</button>
                </form>
                <button onClick={(event) => handleButton(event,"clr-data", "upload")}>Clear Data</button>
                <h2>Files in Database</h2>
                <div className='filebox'>
                    <ListBox input={fileNames}/>
                </div>
                <button onClick={(event) => handleButton(event,"start-chat", "start-chat")}>Chat</button>
                <button onClick={(event) => handleButton(event,"logout", "login")}>Log-out</button>
            </div>
        )
}