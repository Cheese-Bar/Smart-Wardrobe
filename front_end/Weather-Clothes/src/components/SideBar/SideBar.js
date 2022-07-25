import React from "react";
import "./sidebar.css";
import { useHistory } from "react-router-dom";
import { Avatar } from "@material-ui/core";
import { useStateValue } from "../../utils/stateProvider";

const SideBar = () => {

    // Get User info from data layer
    const [{ user }] = useStateValue();
    const history = useHistory();

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
        
    };

    return(

        <div className="side-bar">

            <ul className="side">
                <li><Avatar src={user.photoURL}/></li>
                <li onClick={() => linkAction("/")}>Today's Outfit <span></span></li>
                <li onClick={() => linkAction("/wardrobe")}>Wardrobe <span role="img">👖</span></li>
                <li onClick={() => linkAction("/location")}>Location<span role="img">📍</span></li>
            </ul>

        </div>

    )
}

export default SideBar