import React, {useEffect, useState} from "react";
import { Button } from "@material-ui/core";
import "./login.css";
import { firebase, auth, provider } from "../../utils/firebase";
import { useStateValue } from "../../utils/stateProvider";
import { actionTypes } from "../../utils/reducer";
import anime from 'animejs/lib/anime.es.js';
import { storage } from "../../utils/firebase";
// import sky from "../../images/rack.png";
// import jean from "../../images/jean.png";
// import catImg from "../../images/cat.png";
// import sunImg from "../../images/sun.png";

const LogIn = () => {

    const [catImg, setCatImg] = useState(); 
    console.log("LogIn -> catImg", catImg)
    const [sunImg, setSunImg] = useState();
    console.log("LogIn -> sunImg", sunImg)
    // First we get the viewport height and we multiple it by 1% to get a value for a vh unit
    let vh = window.innerHeight * 0.01;
    // Then we set the value in the --vh custom property to the root of the document
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    useEffect(() => {

            storage
            .ref("myImages")
            .child("cat.png")
            .getDownloadURL()
            .then(url => {
                setCatImg(url)
            })

            storage
            .ref("myImages")
            .child("sun.png")
            .getDownloadURL()
            .then(url => {
                setSunImg(url)
            })

        anime({
            targets: '.login-container > h1',
            keyframes: [
                {opacity: 0},
                {opacity: 10},
                {opacity: 20},
                {opacity: 30},
                {opacity: 40},
                {opacity: 50},
                {opacity: 60},
                {opacity: 70},
                {opacity: 80},
                {opacity: 90},
                {opacity: 100}
              ],
              duration: 10500,
              easing: 'easeInQuad'
          });
        
        anime({
          targets: '.login-container > Button',
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

            <h2 id="title">WW</h2>
            <p>Weather Wear Clothes</p>

            <div className="login-container">
            
                {/* <h2><strong>Weather Wear Clothes</strong></h2> */}
                {/* <img src={jean} alt="mann" height="200px" width="200px"/> */}
                {/* <img src={sky} alt="mann" height="50px" width="30px"/> */}
                <Button size="large" onClick={signIn} style={{opacity: 0}}>Sign In</Button>
                {/* <div><img src={sunImg} alt="sun-icon" id="sun" /></div> */}
                {/* <div><img src={catImg} alt="model" id="model"  /></div> */}

            </div>

        </div>
    )
};

export default LogIn;