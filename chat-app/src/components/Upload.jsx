import React, { useState, useEffect } from "react";
import {ListBox} from "./ListBox"

export const Upload = (props) => {

        const [selectedFile, setSelectedFile] = useState()
        const [isSelected, setIsSelected]= useState(false)

        const [fileNames, setFileNames] = useState([])
        const [hasFileList, setHasFileList] = useState(false)

        const [url, setUrl] = useState()

        const [loadingf, setLoadingf] = useState(false)
        const [loadingu, setLoadingu] = useState(false)

        const handleChange = (event) => {

                setSelectedFile(event.target.files[0]);
                setIsSelected(true);
        }

        const handleSubmitFile = (event) => {
            event.preventDefault()
            setLoadingf(true)

            const formData = new FormData()
            formData.append("file", selectedFile);

            fetch("http://localhost:3000/upload-file",
                {method: "POST",
                body: formData}
            )
            .then(
                response => response.json()
            )
            .then(
                data =>  {
                  if(data.status === 'success'){
                      setFileNames(prevArray => [...prevArray, selectedFile.name]);
                  }
                  else{
                      alert(data.message)
                  }
                  setLoadingf(false)
                }
            )
        }


        const handleSubmitUrl = (event) => {
            event.preventDefault()
            setLoadingu(true)

            const req = {url : url}

            fetch("http://localhost:3000/url-data",
                {method: "POST",
                  headers: { 'Content-Type': 'application/json', 'Accept': 'application/json'},
                  body: JSON.stringify(req)}
            )
            .then(
                response => response.json()
            )
            .then(
                data =>  {
                  if(data.status === 'success'){
                      setFileNames(prevArray => [...prevArray, url]);
                      setUrl('')
                  }
                  else{
                      alert(data.message)
                  }
                  setLoadingu(false)
                }
            )
        }


        const handleButton = (event, loc, page) => {
            fetch("http://localhost:3000/" + loc,
                  {method: "GET"}
            )
            .then(
                  response => response.json()
            ).then(
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
           fetch("http://localhost:3000/get-file-list",
                {method: "GET"}
           )
           .then(
                response => response.json()
           )
           .then(
                data =>  {
                    if(data.status === 'success'){
                        setFileNames(data.files)
                    }
                    else{
                        alert(data.message)
                    }
                }
           )
        }

        useEffect(
            () => {
                getFileNames()
                setFileNames(prevArray => [...prevArray]);
            }
        ,[]);


        return (
            <div className="auth-container">
                <form className="login-form" onSubmit={handleSubmitFile}>
                    <h2>Upload PDF</h2>
                    <input  onChange={(event) => handleChange(event)} type="file" id= 'file' name='file'/>
                    {loadingf ? (<div align='center' className="spinner"></div> ): <button type="submit">Submit</button> }
                </form>
                <form className="login-form" onSubmit={handleSubmitUrl}>
                    <h2>Add Web Data</h2>
                    <input value={url} onChange={(event) => setUrl(event.target.value)} type="url" placeholder="Enter URL" id= 'url' name='url'/>
                    {loadingu ? (<div align='center' className="spinner"></div> ): <button type="submit">Submit</button> }
                </form>
                <h2>Loaded Data</h2>
                <div className='filebox'>
                    <ListBox input={fileNames}/>
                </div>
                <button onClick={(event) => handleButton(event,"clr-data", "upload")}>Clear Data</button>
                <button onClick={(event) => handleButton(event,"start-chat", "start-chat")}>Chat</button>
                <button onClick={(event) => handleButton(event,"logout", "login")}>Log-out</button>
            </div>
        )
}