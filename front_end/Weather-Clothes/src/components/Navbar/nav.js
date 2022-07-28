import React, { useState, useEffect, useContext } from "react";
import "./nav.css";
import SettingsSharpIcon from '@material-ui/icons/SettingsSharp';
import { IconButton, Avatar } from "@material-ui/core";
import { useStateValue } from "../../utils/stateProvider";
import { useHistory } from "react-router-dom";
// import moment from "moment";
import temp from "../../images/temp.png";
import info from "../../images/info.png";
import hum from "../../images/hum.png";
import { UserContext } from "../../utils/UserContext";
import Axios from "axios";
import Login from "../../Pages/LogIn/login";
import server from "../../server";
import Wardrobe from "../../Pages/Wardrobe/wardrobe";

const Navbar = () => {

    // Get User info from data layer
    const [{ user }] = useStateValue();
    // Determine if nav pop is open/closed
    const [navActive, setNavActive] = useState("false");
    // Determine annimation
    const [fadeIn, setFadeIn] = useState(0);
    const history = useHistory();
    const [InTemp, setInTemp] = useState();
    const [InHumidity, setInHumidity] = useState();
    const {setInfoPop, setInfoContent} = useContext(UserContext);

    useEffect(() => {

        // Get today current temperature data
        Axios.get('http://'+server+':9000/getRealData').then(function (res) {
            if(res.data.statu === "success"){
                setInTemp(res.data.indoor.temp);
                setInHumidity(res.data.indoor.humidity);
                console.log("Get current temperature-->GetRealData");
            }else{
                window.confirm("Get data failed!");
            }
        }).catch(function (error) {
            window.confirm("error!");
            console.log(error);
        })
    },[])
    
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

            case "/weather":
                history.push("/weather")
                break;
        
            default:
                break;
        }
        
        toggleNav();
    };


    return(
        <header>

            <nav>

                <div className="bar">
                    
                    <IconButton id="gear" onClick={toggleNav}><SettingsSharpIcon /></IconButton>
                    
                    <p>
                        {
                            (()=> {

                                if (typeof InTemp === "number") {
    
                                    const temperature = "Wardrobe : " + InTemp + " °C";
                                    const humidity = InHumidity;
    
                                    return (
                                        <>
                                            <img src={temp} alt="tempurature-icon" height="25px" width="25px"/>
                                            {temperature+"  "}
                                            <img src={hum} alt="humidity-icon" height = "25px" width="20px"/>
                                            {" " +humidity}
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
                    
                    {/*<li><Avatar src={user.photoURL}/></li>*/}
                    <li onClick={() => linkAction("/weather")}>Weather</li>
                    <li onClick={() => linkAction("/wardrobe")}>Wardrobe</li>
                    <li onClick={() => linkAction("/")}>Today's Outfit</li>
                    <li className="how" onClick={() => {setInfoPop("block"); setInfoContent("how")}}>How to&nbsp;<img src={info} alt="info" width="15" heigh="15"/></li>
                    {/*<li><Button id="sign-out" onClick={signOut}>Sign Out</Button></li>*/}

                </ul>
                    
            </nav>
            
        </header>
    )
}

export default Navbar;