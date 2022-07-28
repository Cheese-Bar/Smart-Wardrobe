import React, { useEffect, useState, useContext } from "react";
import { useStateValue } from "../../utils/stateProvider";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./weather.css";
import { UserContext } from "../../utils/UserContext";
import Chart from "../../components/Chart/chart"
import garmetsBck from "../../images/garmets.png";
// import Swiper JS
import { Swiper, SwiperSlide } from "swiper/react";
import 'swiper/swiper.scss';
import SwiperCore, {Navigation} from 'swiper/core';
import "swiper/components/navigation/navigation.min.css"
import API from "../../utils/API";
import Axios from "axios";
import server from "../../server";
// // install Swiper modules
SwiperCore.use([Navigation]);

const W3 = () => {

    const [{ user }] = useStateValue();
    const [OutTemp, setOutTemp] = useState();
    const [OutHumidity, setOutHumidity] = useState();
    const [OutPressure, setOutPressure] = useState();
    const [InTemp, setInTemp] = useState();
    const [InHumidity, setInHumidity] = useState();
    const {setBck, setInfoPop, setInfoContent} = useContext(UserContext);

    useEffect(() => {
        // Get weather data from API based on city from DB
        Axios.get('http://'+server+':9000/getRealData').then(function (res){
            if(res.data.statu === "success"){
                const In = res.data.indoor;
                const Out = res.data.outdoor;
                setOutTemp(Out.temp);
                setOutHumidity(Out.humidity);
                setOutPressure(Out.pressure);
                setInTemp(In.temp);
                setInHumidity(In.humidity);
                console.log(res.data);
            }else{
                window.confirm("Get data failed!");
            }
        }).catch(function (error) {
            window.confirm("error!");
            console.log(error);
        })
    },[])

    return(
        <div className="weather-page">
            <div className="myDiv">
                <h1>OutDoor Weather</h1>
                <h2>{"Temperature:" + OutTemp +" °C"}</h2>
                <h2>{"Humidity:" + OutHumidity}</h2>
                <h2>{"Pressure:" + OutPressure + " Pa"}</h2>
            </div>;

            <div className = "char">
                <Chart />
            </div>
            <h1 className="chartName"> OutDoor Weather Data & Temperature Prediction</h1>
        </div>
    )
};
export default W3;