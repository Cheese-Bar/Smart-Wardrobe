import React, { useState, useEffect, useContext } from "react";
import "./location.css";
import { useStateValue } from "../../utils/stateProvider";
import { Button } from "@material-ui/core";
import db from "../../utils/firebase";
// import { Toast } from 'react-bootstrap';
import { UserContext } from "../../utils/UserContext";


const Location = () => {

    const [{ user }] = useStateValue();
    const [initialCity, setInitialCity] = useState("City");
    const [newCity, setNewCity] = useState();
    const [id, setId] = useState();
    const cityRef = db.collection("city").where('uid', '==', user.uid);
    const {setBck, setInfoPop, setInfoContent} = useContext(UserContext);

    // Pull user's city from the database
    useEffect(() => {

        setBck("-webkit-linear-gradient(150deg, #ecdfd100 50%, #fcf3ed 50%)");
        // setBck("-webkit-linear-gradient(150deg, #ecdfd100 50%, #e1d4c0 50%)");

        cityRef.onSnapshot(snapshot => {

            const data = snapshot.docs.map((doc) => doc.data())

            // If the DB has a city store it else log no city
            if (data[0]) {
                setInitialCity(data[0].city)
            } else {
                console.log("no city from db")
            }
        })

    //eslint-disable-next-line        
    },[])

    // Pull ID of the doc from firebase
    useEffect(() => {

        db
        .collection("city")
        .get()
        .then((querySnapshot) => {
            querySnapshot.forEach((doc) => {

                setId(doc.id)

            });
        });

    //eslint-disable-next-line
    },[])

    // Send new city input into databae
    const addCity = (newCity) => {

        db.collection("city")
        .add({
            uid: user.uid,
            city: newCity,
        })
        .then(
            alert("Saved")
        )

    };

    // Update city in db according to new user input
    const updateCity = (id, newCity) => {

        db
        .collection("city")
        .doc(id)
        .update({
            city: newCity
        })
        .then(
            setInfoPop("block"),
            setInfoContent("update")
        )

    };

    return(
        <div className="location-page">

            <div className="row text-center">

                <div className="col enter-city">

                    <h1>Enter City</h1>

                    <div>

                        <input placeholder={initialCity || "City"} onChange={(e) => setNewCity(e.target.value)} />
                    
                    </div>

                    <div>

                        {
                        
                        (()=> {

                            if (newCity && initialCity === "City") {

                                return <Button onClick={() => addCity(newCity)}>Submit</Button>;
            
                            }    

                            if (!newCity || newCity === initialCity ) {

                                return <Button disabled>Submit</Button>;}   

                            if (initialCity && initialCity !== newCity) {

                                return <Button onClick={() => updateCity(id, newCity)}>Update</Button>

                        }

                        })()
                        }
                    
                    </div>
                    
                </div>

            </div>
        
            <div className="row"></div>

        </div>
    )

};

export default Location;