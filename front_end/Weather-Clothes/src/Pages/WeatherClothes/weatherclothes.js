import React, {useState, useEffect, useContext} from "react";
import "./weatherclothes.css";
import { useStateValue } from "../../utils/stateProvider";
import moment from "moment";
import Axios from "axios";
import { UserContext } from "../../utils/UserContext";
import server from "../../server";
import info from "../../images/info.png";

const WeatherClothes = () => {

    const [{ user }] = useStateValue();
    const [location, setLocation] = useState();
    const [todaysTemp, setTodaysTemp] = useState();
    // const [todayDescript, setTodayDescript] = useState();
    const [weekDay, setWeekDay] = useState();
    const [outfit, setOutfit] = useState();
    // const outfitSavedDay = localStorage.getItem("today");
    // const [dayCheck, setDayCheck] = useState();
    const [clothName, setClothName] = useState();
    const [clothURL, setClothURL] = useState();
    const [clothType, setClothType] = useState();
    const [bestFit, setBestFit] = useState()
    const {setBck, setInfoPop, setInfoContent} = useContext(UserContext);

    // Weekday Data fetching
    useEffect(() => {

        // Get & set the day of the week
        setWeekDay(moment().format('dddd'));

    //eslint-disable-next-line
    },[])

    // Get outfits from DB

    useEffect(() => {
        Axios.get("http://"+server+":9000/getBestFit").then(function (res){
            if (res.data.statu === "success"){
                setClothName(res.data.bestfit[0]);
                setClothURL(res.data.bestfit[1]);
                setClothType(res.data.bestfit[2]);
                setBestFit(function () {
                    return[{"name": clothName, "url": clothURL, "type":clothType}]
                })
                console.log(res.data.bestfit);
            }else {
                console.log(res.data.statu);
            }
            // console.log(best)
        }).catch(function (error) {
            window.confirm("error!");
            console.log(error);
        })
    },[])


    // const todaysFit = () => {
    //     if (noFits === true) {
    //         return (
    //         <div className="how" onClick={() => {setInfoPop("block"); setInfoContent("how");}}>
    //             <h3 >How to</h3>&nbsp;<img src={info} alt="info" width="15" heigh="15"/>
    //         </div>
    //         )
    //     }
    //     if (noFits === false) {
    //         return (
    //             <div>
    //                 <div>
    //                     <img src={clothURL} alt="outfit" height="300px" width="auto"/>
    //                 </div>
    //                 <p>{clothName+"("+clothType+")"}</p>
    //             </div>
    //         )
    //     }
    // };


    return(
        
        <>
            <div className="container">
                {
                    // Row 1 - Weekdays list
                }
                <div className="row text-center">
                    
                    <div className="col-12">

                        <ul className="day-list">

                            <li className={weekDay === "Monday" ? "current-day" : "days"}>M</li>
                            <li className={weekDay === "Tuesday" ? "current-day" : "days"}>T</li>
                            <li className={weekDay === "Wednesday" ? "current-day" : "days"}>W</li>
                            <li className={weekDay === "Thursday" ? "current-day" : "days"}>T</li>
                            <li className={weekDay === "Friday" ? "current-day" : "days"}>F</li>
                            <li className={weekDay === "Saturday" ? "current-day" : "days"}>S</li>
                            <li className={weekDay === "Sunday" ? "current-day" : "days"}>S</li>

                        </ul>

                    </div>
                    
                </div>

                {
                    // Row 2 - Outfit for today
                }
                <div className="row text-center">

                    <div className="col"></div>

                    <div className="col">

                        <h1 >Today's Outfit</h1>
                        <hr />
                        {
                            !bestFit ? (
                                <div className="how" onClick={() => {setInfoPop("block"); setInfoContent("how");}}>
                                    <h3 >How to</h3>&nbsp;<img src={info} alt="info" width="15" heigh="15"/>
                                </div>
                            )
                            :bestFit?.map(items =>
                            <div>
                                <img src={clothURL} alt="outfit" height="300px" width="auto"/>
                                <h3>{"Name: " + clothName}</h3>
                                <h3>{"Type: " + clothType}</h3>
                            </div>
                                )
                        }
                    </div>

                    <div className="col"></div>

                </div>

                <div className="day-page"></div>

            </div>
        </>
        
    )
};

export default WeatherClothes;