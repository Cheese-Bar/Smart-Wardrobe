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

    useEffect(() => {

        setBck(`url(${garmetsBck})`);

    },[setBck])

    // TODO: 改上传图片方法
    const handleImgUpload = (event) => {

        // event.preventDefault()
        //
        // // Upload image to firestore and store in variable
        // // const uploadTask = storage.ref(`images/${fitImage.name}`).put(fitImage);
        //
        // // Get url of image just uploaded to firestore storage
        // uploadTask.on(
        //     "state_changed",
        //     snapshot => {},
        //     error => {
        //         console.log(error)
        //     },
        //     () => {
        //         storage
        //         .ref("images")
        //         .child(fitImage.name)
        //         .getDownloadURL()
        //         .then(url =>
        //             setImgUrl(url)
        //         )
        //     }
        // )
        // setInfoPop("block");
        // setInfoContent("img")

    };

    const addOutfit = () => {

        wardrobeRef.add(
            {
                uid: user.uid,
                outfit: outfitName,
                weather: fitWeather,
                temperature: fitTemp,
                image: imgUrl,
                context: fitContext
            }
        ).then(history.push('/wardrobe'))
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
                        <button onClick={(event) => {handleImgUpload(event)}} id="upload-button">Upload</button>
                        
                        <br/>
                        <br/>

                        {// Get Weather description input for oufit
                        }
                        <select className="custom-select" style={{width: "133px"}} onChange={(e) => {
                            setFitWeather(e.target.value)
                        }}>
                            <option></option>
                            <option value="clear Sky" className="select-items">Clear Sky</option>
                            <option value="overcast">Overcast</option>
                            <option value="rain">Rain</option>
                            <option value="sunny">Sunny</option>
                        </select>

                        <select className="custom-select" style={{width: "133px"}} onChange={(e) => {
                            setFitTemp(e.target.value)
                        }}>
                            <option></option>
                            <option value="neutral">Neutral</option>
                            <option value="hot">Hot</option>
                            <option value="cold">Cold</option>
                        </select>

                        <select className="custom-select" style={{width: "133px"}} onChange={(e) => {
                            setFitContext(e.target.value)
                        }}>
                            <option></option>
                            <option value="home">Home</option>
                            <option value="work">Work</option>
                            <option value="casual">Casual</option>
                        </select>

                        <br/>
                        <br/>

                        {// If there is no outfit name and details disable submit button otherwise enable
                        }
                        {
                        outfitName && fitWeather && fitTemp && imgUrl && fitContext  ? 
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