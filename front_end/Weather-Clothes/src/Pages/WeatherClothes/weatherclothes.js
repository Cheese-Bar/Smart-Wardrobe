import React, {useState, useEffect, useContext} from "react";
import "./weatherclothes.css";
import db from "../../utils/firebase";
import { useStateValue } from "../../utils/stateProvider";
import moment from "moment";
import API from "../../utils/API";
import { UserContext } from "../../utils/UserContext";
import info from "../../images/info.png";

const WeatherClothes = () => {

    const [{ user }] = useStateValue();
    const [location, setLocation] = useState();
    const [todaysTemp, setTodaysTemp] = useState();
    // const [todayDescript, setTodayDescript] = useState();
    const [weekDay, setWeekDay] = useState();
    const [outfit, setOutfit] = useState();
    const outfitSavedDay = localStorage.getItem("today");
    // const [dayCheck, setDayCheck] = useState();
    const [noFits, setNoFits] = useState();
    const {setBck, setInfoPop, setInfoContent} = useContext(UserContext);

    // Location, Weather & Weekday Data fetching
    useEffect(() => {

        // setBck(`url(${garmetsBck})`);
        setBck("-webkit-linear-gradient(150deg, #ecdfd100 50%, #fcf3ed 50%)");

        // Get location data from DB
        db
        .collection("city")
        .where('uid', '==', user.uid)
        .onSnapshot(snapshot => setLocation(snapshot.docs.map((doc) => doc.data().city)))

        // Get & set the day of the week
        setWeekDay(moment().format('dddd'));

    //eslint-disable-next-line
    },[])

    useEffect(() => {

        // Get weather data from API based on city from DB
        API.search(location)
        .then((res) => {
            console.log(res)
            setTodaysTemp(res.data.list[0].main.temp)
        })

    },[location])

    useEffect(() => {

        console.log(moment().format('dddd'))
        console.log("outfitsaved day --->" + outfitSavedDay)


        if (moment().format('dddd') !== outfitSavedDay) {
            console.log("days dont match!")
            localStorage.removeItem("todaysOutfit");
            localStorage.removeItem("today");
            return
        }
        else {
            
            console.log("Days DO match!")
        }

        // setDayCheck(true);

        
    }, [weekDay, outfitSavedDay])

    const determineOutfit = (hotFits, neutralFits, coldFits) => {

        if (!todaysTemp) setOutfit("No Outfit Loading (out of API calls)");
        else {
            if (todaysTemp => 70) {
            const hotfitNum = hotFits.length
            const randomHotFitNum = (Math.floor(Math.random() * hotfitNum));
            setOutfit(hotFits[randomHotFitNum].image);
            localStorage.setItem("todaysOutfit", hotFits[randomHotFitNum].image)
            localStorage.setItem("today", weekDay)
            }
            if (todaysTemp > 70 && todaysTemp > 68) {
                const randomNeutralFitNum = (Math.floor(Math.random() * neutralFits.length));
                setOutfit(neutralFits[randomNeutralFitNum].image);
                localStorage.setItem("todaysOutfit", neutralFits[randomNeutralFitNum].image)
                localStorage.setItem("today", weekDay)
            }
            if (todaysTemp > 68 ) {
                const randomColdFitNum = (Math.floor(Math.random() * coldFits.length));
                setOutfit(coldFits[randomColdFitNum].image)
                localStorage.setItem("todaysOutfit", coldFits[randomColdFitNum].image)
                localStorage.setItem("today", weekDay)
            }
        }

    };

    const storeDbVals = (snapshot) => {
        const fits = snapshot.docs.map((doc) => doc.data());
        const hotFits = fits.filter(fit => fit.temperature === "hot");
        const neutralFits = fits.filter(fit => fit.temperature === "neutral");
        const coldFits = fits.filter(fit => fit.temperature === "cold");
        determineOutfit(hotFits, neutralFits, coldFits);
    };

    // Get outfits from DB
    const queryDb = () => {

        db
        .collection("wardrobe")
        .where('uid', '==', user.uid)
        .onSnapshot(snapshot => {

            const snap = snapshot.docs.map((doc) => doc.data());
            console.log("snap: " + snap);

            if (snap.length === 0) {
                setNoFits(true);
            }
            if (snap.length > 0) {
                setNoFits(false);
                storeDbVals(snapshot)
            }

        });

    };
    
    useEffect(() => {

        const savedOutfit = localStorage.getItem("todaysOutfit");

        // If there is an outfit saved in local storage set it to Outfit state else determine a new one
        savedOutfit ? setOutfit(savedOutfit) : queryDb()

        console.log(savedOutfit);
        
    //eslint-disable-next-line
    },[]);

    const todaysFit = () => {
        if (noFits === true) {
            return (
            <div className="how" onClick={() => {setInfoPop("block"); setInfoContent("how");}}>
                <h3>How to</h3>&nbsp;<img src={info} alt="info" width="15" heigh="15"/>
            </div>
            )
        }
        if (noFits === false) {
            return (
            outfit === "No Outfit Loading (out of API calls)" ? <p>{outfit}</p> 
            :
            <img src={outfit} alt="oufit" height="300px" width="auto"/>
            )
        }                
    };


    return(
        
        <>
            {console.log(`no fit: ${noFits}, outfit: ${outfit}`)}
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

                        <h1>Today's Outfit</h1>
                        <hr />
                        {todaysFit()}

                    </div>

                    <div className="col"></div>

                </div>

                <div className="day-page"></div>

            </div>
        </>
        
    )
};

export default WeatherClothes;