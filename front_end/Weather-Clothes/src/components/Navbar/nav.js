import React, { useState, useEffect, useContext } from "react";
import "./nav.css";
import SettingsSharpIcon from '@material-ui/icons/SettingsSharp';
import { IconButton, Avatar } from "@material-ui/core";
import { useStateValue } from "../../utils/stateProvider";
import { useHistory } from "react-router-dom";
// import moment from "moment";
import { auth } from "../../utils/firebase";
import { Button } from "@material-ui/core";
import API from "../../utils/API";
import db from "../../utils/firebase";
import temp from "../../images/temp.png";
import info from "../../images/info.png";
import { UserContext } from "../../utils/UserContext";

const Navbar = () => {

    // Get User info from data layer
    const [{ user }] = useStateValue();
    // Determine if nav pop is open/closed
    const [navActive, setNavActive] = useState("false");
    // Determine annimation
    const [fadeIn, setFadeIn] = useState(0);
    const history = useHistory();
    const [location, setLocation] = useState();
    const [todaysTemp, setTodaysTemp] = useState();
    const [todayDescript, setTodayDescript] = useState();
    const {setInfoPop, setInfoContent} = useContext(UserContext);

    useEffect(() => {

        // Get location data from DB
        db
        .collection("city")
        .where('uid', '==', user.uid)
        .onSnapshot(snapshot => setLocation(snapshot.docs.map((doc) => doc.data().city)))
        
    //eslint-disable-next-line    
    },[])

    useEffect(() => {

        // Get weather data from API based on city from DB
        API.search(location)
        .then((res) => {
            setTodaysTemp(res.data.list[0].main.temp)
            setTodayDescript(res.data.list[0].weather[0].description)
        })

    },[location])
    
    // Toggle Our Navigation Bar
    const toggleNav = () => {

        if (navActive === "true") {
            setNavActive("false")
            setFadeIn(0)
        } else {
            setNavActive("true")
            setFadeIn(1)
        }

    };

    // Click handle events for nav links
    const linkAction = (link) => {

        switch (link) {
            case "/":
                history.push("/")
                break;

            case "/wardrobe":
                history.push("/wardrobe")
                break;

            case "/add":
                history.push("/add")
                break;
            
            case "/location":
                history.push("/location")
                break;    
        
            default:
                break;
        }
        
        toggleNav();
    };

    // Convert kelvin temp to faranheight
    const kelvinToFaran = (kelvin) => {
        return (kelvin - 273.15) * 9/5 + 32
    };

    const signOut = () => {
        auth.signOut()
    };

    return(
        <header>

            <nav>

                <div className="bar">
                    
                    <IconButton id="gear" onClick={toggleNav}><SettingsSharpIcon /></IconButton>
                    
                    <p>
                        {
                            (()=> {

                                if (typeof todaysTemp === "number") {
    
                                    const temperature = Math.round(kelvinToFaran(todaysTemp)) + "°";
    
                                    return (
                                        <>
                                            <img src={temp} alt="tempurature-icon" height="25px" width="25px"/>
                                            {temperature + " " + todayDescript}
                                        </>
                                    )
                                }
                                else {
    
                                    return 0
    
                                }
                                })()
                        }
                        {/* {moment().format("MMM Do YY")} */}
                    </p>

                </div>

                <ul className={`nav-links ${navActive === "true" ? "nav-active" : ""}`} fadein={fadeIn} onAnimationEnd={() => {setFadeIn(0)}}>
                    
                    <li><Avatar src={user.photoURL}/></li>
                    <li onClick={() => linkAction("/location")}>Location</li>
                    <li onClick={() => linkAction("/wardrobe")}>Wardrobe</li>
                    <li onClick={() => linkAction("/")}>Today's Outfit</li>
                    <li className="how" onClick={() => {setInfoPop("block"); setInfoContent("how")}}>How to&nbsp;<img src={info} alt="info" width="15" heigh="15"/></li>
                    <li><Button id="sign-out" onClick={signOut}>Sign Out</Button></li>

                </ul>
                    
            </nav>
            
        </header>
    )
}

export default Navbar;