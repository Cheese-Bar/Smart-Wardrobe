import React, { useEffect, useState, useContext } from "react";
import "./addoutfit.css";
import { useStateValue } from "../../utils/stateProvider";
import db from "../../utils/firebase";
import { Button } from "@material-ui/core";
import { useHistory } from "react-router-dom";
import { storage } from "../../utils/firebase";
// import { Toast } from 'react-bootstrap';
import garmetsBck from "../../images/garmets.png";
import { UserContext } from "../../utils/UserContext";
import server from "../../server";
import Axios from "axios";

const AddOutfit = () => {

    // Get loggedin user info
    const [{ user }] = useStateValue();
    const history = useHistory();
    // Get colleection from firebase
    const wardrobeRef = db.collection("wardrobe");
    const [outfitName, setOutfitName] = useState();
    const [fitImage, setFitImage] = useState();
    const [imgUrl, setImgUrl] = useState();
    const [fitWeather, setFitWeather] = useState();
    const [fitTemp, setFitTemp] = useState();
    const [fitContext, setFitContext] = useState();
    const {setBck, setInfoPop, setInfoContent} = useContext(UserContext);


    // // TODO: 改上传图片方法
    // const handleImgUpload = (event) => {
    //
    //     Axios.post("http://10.24.239.172:9000/uploadImage",{name: outfitName,url: imgUrl})
    //
    //     event.preventDefault()
    //
    //     // Upload image to firestore and store in variable
    //     // const uploadTask = storage.ref(`images/${fitImage.name}`).put(fitImage);
    //
    //     // Get url of image just uploaded to firestore storage
    //     uploadTask.on(
    //         "state_changed",
    //         snapshot => {},
    //         error => {
    //             console.log(error)
    //         },
    //         () => {
    //             storage
    //             .ref("images")
    //             .child(fitImage.name)
    //             .getDownloadURL()
    //             .then(url =>
    //                 setImgUrl(url)
    //             )
    //         }
    //     )
    //     setInfoPop("block");
    //     setInfoContent("img")
    //
    // };

    const addOutfit = () => {
        let formData = new FormData();
        formData.append("name", outfitName);

        formData.append("upload", fitImage);

        Axios.post("http://"+server+":9000/uploadImage", formData)
            .then(function (res) {
                if(res.data.statu === "success"){
                    history.push('/wardrobe');
                    console.log("add out fit success");
                }else{
                        window.confirm("Add outfit failed!");
                    }
                }).catch(function (error) {
                    window.confirm("error!");
                    console.log(error);
                })
    };

    return(

        <div className="add-page">

            <div className="row text-center">

                <div className="col">
                    
                    <form>

                        {//Outfit Name Entry
                        }
                        <h1 id="enter-fit">Enter Outfit</h1>
                        <p><em>lay out your outfit and take a photo!</em></p>
                        <input type="text" placeholder="Name Your Outfit" 
                        onChange={(e) => setOutfitName(e.target.value)} id="fit-input"></input>
                        
                        <br/>
                        <br/>

                        <input type="file" accept="image/*" onChange={(event) => setFitImage(event.target.files[0])} id="img-upload"></input>
                        {/*<button onClick={(event) => {handleImgUpload(event)}} id="upload-button">Upload</button>*/}

                        <br/>
                        <br/>

                        {// If there is no outfit name and details disable submit button otherwise enable
                        }
                        {
                        outfitName && fitImage  ?
                        <Button onClick={() => addOutfit()}>Submit</Button>
                        :
                        <Button disabled>Submit</Button>
                        }
                        
                    </form>

                </div>

            </div>

            <div className="row"></div>

        </div>
        
        )

};

export default AddOutfit;