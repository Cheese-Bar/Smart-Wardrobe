import React, {useEffect, useState} from "react";
import {Button, colors} from "@material-ui/core";
import "./login.css";
import { firebase, auth, provider } from "../../utils/firebase";
import { useStateValue } from "../../utils/stateProvider";
import { actionTypes } from "../../utils/reducer";
import anime from 'animejs/lib/anime.es.js';
import { storage } from "../../utils/firebase";
import Axios from "axios";
import { useHistory } from "react-router-dom";
// import sky from "../../images/rack.png";
// import jean from "../../images/jean.png";
// import catImg from "../../images/cat.png";
// import sunImg from "../../images/sun.png";

const LogIn = () => {

    const history = useHistory()

    const [catImg, setCatImg] = useState();
    console.log("LogIn -> catImg", catImg)
    const [sunImg, setSunImg] = useState();
    console.log("LogIn -> sunImg", sunImg)
    // First we get the viewport height and we multiple it by 1% to get a value for a vh unit
    let vh = window.innerHeight * 0.01;
    // Then we set the value in the --vh custom property to the root of the document
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    useEffect(() => {

        anime({
            targets: '.login-container > div',
            keyframes: [
                {translateY: 500},
                {opacity: 100},
                {translateY: 0},
            ],
            duration: 1000,
            easing: 'easeInQuad'
        });

        anime({
            targets: '.login-container > button',
            keyframes: [
                {translateY: 500},
                {opacity: 100},
                {translateY: 0},
            ],
            duration: 1000,
            easing: 'easeInQuad'
        });

    },[])

    const [dispatch] = useStateValue();

    const signIn = () => {

        let name = document.getElementById("user").value;
        let password = document.getElementById("registerpwd").value;

        // if(name === "123" && password === "456"){
        //     window.location.href='/addOutfit';
        // }

        Axios.post("http://10.15.198.144:9000/login",{name: name,pwd: password})
            .then(function (response) {
            console.log(response);
            history.push("/login");
        })
            .catch(function (error) {
                console.log(error);
                window.alert("Name or Password Error!");
            });

        auth
        .setPersistence(firebase.auth.Auth.Persistence.LOCAL)
        .then(() => {

            auth.signInWithPopup(provider)
            .then(result => {
            dispatch({
                type: actionTypes.SET_USER,
                user: result.user
            })
        })
        .catch(err => console.log(err.message))

        })

    };

    return(
        <div className="login">

            <h2 id="title">Smart Wardrobe</h2>

            <div className="login-container" >
                <div className="userdiv">
                    <input id="user" className="signinput"  type="text"  placeholder="Name" name="user"/>
                </div>

                <div className="pwddiv">
                    <input id="registerpwd" className="signinput"  type="password" placeholder="Password" name="pwd"/>
                </div>
                {/* <h2><strong>Weather Wear Clothes</strong></h2> */}
                {/* <img src={jean} alt="mann" height="200px" width="200px"/> */}
                {/* <img src={sky} alt="mann" height="50px" width="30px"/> */}
                <Button size="large" onClick={signIn} style={{opacity: 0}}>Sign In</Button>
                 {/*<div><img src={sunImg} alt="sun-icon" id="sun" /></div>*/}
                {/* <div><img src={catImg} alt="model" id="model"  /></div> */}

            </div>

        </div>
    )
};

export default LogIn;