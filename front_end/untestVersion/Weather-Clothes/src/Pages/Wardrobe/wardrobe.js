import React, { useEffect, useState, useContext } from "react";
import db from "../../utils/firebase";
import { useStateValue } from "../../utils/stateProvider";
import AddOutlinedIcon from '@material-ui/icons/AddOutlined';
import { IconButton } from "@material-ui/core";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { useHistory } from "react-router-dom";
import "./wardrobe.css";
import hanger from "../../images/hanger.png";
import closet from "../../images/closet.png";
import { UserContext } from "../../utils/UserContext";
import garmetsBck from "../../images/garmets.png";
// import Swiper JS
import { Swiper, SwiperSlide } from "swiper/react";
import 'swiper/swiper.scss';
import SwiperCore, {Navigation} from 'swiper/core';
import "swiper/components/navigation/navigation.min.css"
import Axios from "axios";
import server from "../../server";
// // install Swiper modules
SwiperCore.use([Navigation]);

const W2 = () => {

    // Get loggedin user info
    let index = 0;
    const [{ user }] = useStateValue();
    const [noFits, setNoFits] = useState();
    // const [outfits, setOutfits] = useState();
    const history = useHistory();
    const {setBck} = useContext(UserContext);

    var outfits = []

    // Get outfits
    useEffect(() => {

        Axios.get("http://"+server+":9000/getAll").then(function (res) {
            if(res.data.statu === "success"){
                if(res.data.All.length === 0){
                    setNoFits(true);
                    console.log(res.data.All);
                }else {
                    setNoFits(false);
                    outfits = res.data.All;
                    console.log(res.data.All);
                }
            }else{
                window.confirm("Get data failed! ")
            }
        }).catch(function (error){
            window.confirm("error!");
        })
    //eslint-disable-next-line
    },[index]);


    // const createSlide = (doc) =>{
    //     return (
    //         < SwiperSlide className="swiper-slide" key={doc.id}>
    //         <h1 id="fit-name">{doc.name}</h1>
    //         <IconButton key={doc.id} onClick={() => removeFit(doc.id)}>
    //             <img src={hanger} alt="hanger" width="25" height="25" id="hang"/>
    //         </IconButton>
    //         <img src={doc.url} alt="outfit" id="fit-pic"/>
    //         </SwiperSlide>
    //     )
    // }

    //remove cloth
    const removeFit = (id) => {
        let confirmDl = window.confirm("delete?")
        if (confirmDl){
            Axios.get("http://"+server+"9000/deleteImage/"+id)
                .then(function (res){
                    if(res.data.statu === "success"){
                        index = id;
                    }else{
                        window.confirm("remove failed!")
                    }
                }).catch(function (error) {
                window.confirm("error!");
            })
        }
    };

    // retreive slide # var from css
    let num = getComputedStyle(document.documentElement).getPropertyValue('--slideNum');

    return(
        <div className="wardrobe-page">
            <Swiper navigation={true} spaceBetween={50} slidesPerView={num} onSlideChange={() => console.log('slide change')} className="mySwiper">
                        {
                            outfits.map((outfits) =>
                                (<SwiperSlide  className="swiper-slide" key={outfits.id}>
                                    <h1 id="fit-name">{outfits.name}</h1>
                                    <IconButton key={outfits.id} onClick={() => removeFit(outfits.id)}>

                                        <img src={hanger} alt="hanger" width="25" height="25" id="hang"/>
                                    </IconButton>

                                    <img src={outfits.url} alt="outfit" id="fit-pic"/>
                                </SwiperSlide>)
                            )
                        }

            </Swiper>

             <div className="add-fit">
                <img src={closet} alt="closet"/><br/>
                <IconButton onClick={() => history.push("/add")}><AddOutlinedIcon /></IconButton>
                <p>Add Outfit</p>
            </div>

        </div>
    )
};

export default W2;