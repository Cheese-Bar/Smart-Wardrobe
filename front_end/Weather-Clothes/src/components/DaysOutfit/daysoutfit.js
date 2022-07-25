import React from "react";

const DaysOutfit = (props) => {

    return(<>
    <h1>{props.name}</h1>
    <div><img src={props.image} alt="outfit img"></img></div>
    </>)
    
};

export default DaysOutfit;