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
                }else{
                    window.confirm("Get data failed!");
                }
            }).catch(function (error) {
                window.confirm("error!");
            })
    },[])

    let option = {
        tooltip: {trigger: 'axis'},
        legend: {},
        toolbox: {
            show: true,
            feature: {
                dataZoom: {yAxisIndex: 'none'},
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                restore: {},
                saveAsImage: {}
            }
        },
        textStyle: {fontSize: 25},
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,21, 22, 23, 24]
        },
        yAxis: {
            type: 'value',
            axisLabel: {formatter: '{value} °C'}
        },
        series: [
            {
                name: 'Temperature',
                type: 'line',
                color: '#3ba272',
                smooth: 'true',
                data: [],
                markPoint: {
                    symbolSize: 100,
                    data: [{ name: 'prediction', value: 0, xAxis: 24, yAxis:  - 1.5 }]
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
    return (<div id = "chart">
        <ReactECharts option={option} />
    </div>);
}

export default Chart;