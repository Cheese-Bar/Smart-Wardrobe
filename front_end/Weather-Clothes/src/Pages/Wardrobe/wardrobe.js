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
// // install Swiper modules
SwiperCore.use([Navigation]);

const W2 = () => {

    // Get loggedin user info
    const [{ user }] = useStateValue();
    const [outfits, setOutfits] = useState();
    const history = useHistory();
    const {setBck} = useContext(UserContext);

    // Get outfits
    useEffect(() => {

        setBck(`url(${garmetsBck})`);
        
        db
        .collection("wardrobe")
        .where('uid', '==', user.uid)
        .onSnapshot(snapshot => setOutfits(snapshot.docs.map((doc) => doc)))

    //eslint-disable-next-line
    },[]);

    const removeFit = (theDoc) => {

      let confirmDl = window.confirm("delete?")

        if (confirmDl) {
            db
            .collection("wardrobe")
            .doc(theDoc)
            .delete()
            .then(() => {
                console.log("Document successfully deleted!");
                
            }).catch((error) => {
                console.error("Error removing document: ", error);
            });
        }
        else {
            console.log("good save")
        }

    };

    // retreive slide # var from css
    let num = getComputedStyle(document.documentElement).getPropertyValue('--slideNum');

    return(
        <div className="wardrobe-page">
            <Swiper navigation={true} spaceBetween={50} slidesPerView={num} onSlideChange={() => console.log('slide change')} className="mySwiper">


                        {
                        outfits ? 
                            outfits.map(doc => 

                                <SwiperSlide  className="swiper-slide" key={doc.id}>
                                    <h1 id="fit-name">{doc.data().outfit}</h1>
                                    <IconButton key={doc.id} onClick={() => removeFit(doc.id)}>
                    
                                        <img src={hanger} alt="hanger" width="25" height="25" id="hang"/>
                                    </IconButton>
                                    
                                    <img src={doc.data().image} alt="outfit" id="fit-pic"/> 
                                </SwiperSlide>

                        ) 
                        : 
                        <p>Add outfits</p>
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