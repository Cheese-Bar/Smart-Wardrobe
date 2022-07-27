import React, { useState, useEffect, useContext } from "react";
// import "./chart.css";
import ReactECharts from "echarts-for-react";
import Axios from "axios";
import server from "../../server";
import {useStateValue} from "../../utils/stateProvider";
import {UserContext} from "../../utils/UserContext";

const Chart = () =>{
    const [temp_list, setTemp_list] = useState();
    const [humidity_list, setHumidity_list] = useState();
    const [pressure_list, setPressure_list] = useState();
    const [prediction, setPrediction] = useState();

    useEffect(()=>{
        Axios.get("http://"+server+":9000/getHistory")
            .then(function (res){
                if(res.data.statu === "success"){
                    setTemp_list(res.data.temp_list);
                    setHumidity_list(res.data.humi_list);
                    setPressure_list(res.data.pres_list);
                    setPrediction(res.data.pred_temp);
                    console.log(res.data);
                }else{
                    window.confirm("Get data failed!");
                }
            }).catch(function (error) {
                window.confirm("error!");
            console.log(error);
            })
    },[])

    const colors = ['#5470C6', '#91CC75', '#EE6666'];
    let option = {
        color: colors,
        tooltip: { trigger: 'axis' },
        grid: {
            left: '20%'
        },
        legend: {},
        toolbox: {
            show: true,
            feature: {
                dataZoom: { yAxisIndex: 'none' },
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                saveAsImage: {}
            }
        },
        textStyle: { fontSize: 13 },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24
            ]
        },
        yAxis: [
            {
                type: 'value',
                position: 'right',
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: colors[2]
                    }
                },
                axisLabel: { formatter: '{value} °C' }
            },
            {
                type: 'value',
                position: 'left',
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: colors[0]
                    }
                },
                axisLabel: { formatter: '{value}' }
            },
            {
                type: 'value',
                position: 'left',
                offset: 80,
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: colors[1]
                    }
                },
                axisLabel: { formatter: '{value} Pa' }
            }
        ],
        series: [
            {
                name: 'Humidity',
                type: 'bar',
                yAxisIndex: 1,
                data: humidity_list,
            },
            {
                name: 'Pressure',
                type: 'scatter',
                yAxisIndex: 2,
                data: pressure_list,
            },
            {
                name: 'Temperature',
                type: 'line',
                smooth: 'true',
                yAxisIndex: 0,
                data: temp_list,
                markPoint: {
                    symbolSize: 50,
                    data: [{ name: 'prediction', value: prediction, xAxis: 24, yAxis: prediction }]
                },
                lineStyle: {
                    width: 4
                }
            }
        ]
    };


    return (<div id = "chart">
        <ReactECharts option={option} />
    </div>);
}

export default Chart;