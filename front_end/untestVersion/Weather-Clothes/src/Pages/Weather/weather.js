import React, { useEffect, useState, useContext } from "react";
import * as echarts from 'echarts';
import db from "../../utils/firebase";
import { useStateValue } from "../../utils/stateProvider";
import AddOutlinedIcon from '@material-ui/icons/AddOutlined';
import { IconButton } from "@material-ui/core";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { useHistory } from "react-router-dom";
import "./weather.css";
import hanger from "../../images/hanger.png";
import closet from "../../images/closet.png";
import { UserContext } from "../../utils/UserContext";
import garmetsBck from "../../images/garmets.png";
// import Swiper JS
import { Swiper, SwiperSlide } from "swiper/react";
import 'swiper/swiper.scss';
import SwiperCore, {Navigation} from 'swiper/core';
import "swiper/components/navigation/navigation.min.css"
import API from "../../utils/API";
import Axios from "axios";
// // install Swiper modules
SwiperCore.use([Navigation]);

const W3 = () => {

    const [{ user }] = useStateValue();
    const [OutTemp, setOutTemp] = useState();
    const [OutHumidity, setOutHumidity] = useState();
    const [OutPressure, setOutPressure] = useState();
    const {setBck, setInfoPop, setInfoContent} = useContext(UserContext);

    useEffect(() => {

        // Get weather data from API based on city from DB
        setOutTemp(Axios.get("http://localhost:3000/weather/temp"));
        setOutHumidity(Axios.get("http://localhost:3000/weather/humidity"));
        setOutPressure(Axios.get("http://localhost:3000/weather/pressure"));
    },[])

    var list = []
    useEffect(()=>{
        Axios.get("http://localhost:3000/weather/25")
            .then(function (res){
                list = res.data;
            })
    })

    const chartDom = document.getElementById('chart');
    const myChart = echarts.init(chartDom);
    var option;

    option = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {},
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                restore: {},
                saveAsImage: {}
            }
        },
        textStyle: {
            fontSize: 25
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24
            ]
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} °C'
            }
        },
        series: [
            {
                name: 'Temperature',
                type: 'line',
                color: '#3ba272',
                smooth: 'true',
                data: list,
                markPoint: {
                    symbolSize: 100,

                    data: [{ name: 'prediction', value: 26, xAxis: 24, yAxis: -1.5 }]
                },
                lineStyle: {
                    width: 4
                },
                markLine: {
                    data: [
                        { type: 'average', name: 'Avg' },
                        [
                            {
                                symbol: 'none',
                                x: '90%',
                                yAxis: 'max'
                            },
                            {
                                symbol: 'circle',
                                label: {
                                    position: 'start',
                                    formatter: 'Max'
                                },
                                type: 'max',
                                name: 'Max'
                            }
                        ]
                    ]
                }
            }
        ]
    };

    option && myChart.setOption(option);


    return(
        <div className="weather-page">
            <div id="myDiv"><h2>{OutTemp+','+OutHumidity+','+OutPressure}</h2></div>
            <div id = "chart">Temperature Prediction</div>
        </div>
    )
};

export default W3;