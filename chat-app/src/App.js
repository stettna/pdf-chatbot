import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import "./App.css";



function LoginForm() {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm();

    const onSubmit = (data) => {
        const userData = JSON.parse(localStorage.getItem(data.email));
        if (userData) { // getItem can return actual value or null
            if (userData.password === data.password) {
                console.log(userData.name + " You Are Successfully Logged In");
            } else {
                console.log("Email or Password is not matching with our record");
            }
        } else {
            console.log("Email or Password is not matching with our record");
        }
    };
    return (
        <>
            <p className="title">Login Form</p>

            <form className="App" onSubmit={handleSubmit(onSubmit)}>
                <input type="email" {...register("email", { required: true })} />
                {errors.email && <span style={{ color: "red" }}>
                    *Email* is mandatory </span>}
                <input type="password" {...register("password")} />
                <input type={"submit"} style={{ backgroundColor: "#a1eafb" }} />
            </form>
        </>
    );
}

function AddData() {
  return (
    <button>
      Add Data
    </button>
  );
}

function form () {
return(
<>
    <form>
        <input type='text' required></input>
        <input type='submit'></input>
    </form>
 </>)
}

function Chat() {
  return (
    <button>
     Chat
    </button>
  );
}

function SignUp() {
  return (
    <button>
      Sign-up
    </button>
  );
}

function Logout() {
  return (
    <button>
      Logout
    </button>
  );
}

function Login() {
  return (
    <button onClick= {LoginForm}>
      Login
    </button>
  );
}

function App() {
  return (
    <div className="App">
    <h1>ChatBot in progress!</h1>
    <Logout />
    <Login />
    <SignUp />
    <Chat />
    <AddData />
    <form />
    </div>
  );
}

export default App;
