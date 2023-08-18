import React, { useState, useEffect} from "react";
import "./App.css";
import {Login} from "./components/Login"
import {Signup} from "./components/Signup"
import {Upload} from "./components/Upload"
import {Chat} from "./components/Chat"

function selectForm(form, toggleForm ) {
  switch (form) {
    case 'login':
      return <Login onFormSwitch={toggleForm} />;
    case 'signup':
      return <Signup onFormSwitch={toggleForm} />;
    case 'upload':
      return <Upload onFormSwitch={toggleForm} />;
    case 'start-chat':
      return <Chat onFormSwitch={toggleForm} />;
    default:
      return null;
  }
}

function App() {
  const [currentForm, setCurrentForm] = useState('login');

  const toggleForm = (form) => {
    setCurrentForm(form);
  }

  return (
    <div className="App">
    {
       selectForm(currentForm, toggleForm)
    }
    </div>
  );
}

export default App;
