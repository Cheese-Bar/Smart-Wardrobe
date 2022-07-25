import firebase from "firebase";
import "firebase/storage"

const firebaseConfig = {
    apiKey: "AIzaSyABq4T8AGbIDOc2ZJMewwYp3XNVzanTjC4",
    authDomain: "weatherclothes-66103.firebaseapp.com",
    databaseURL: "https://weatherclothes-66103.firebaseio.com",
    projectId: "weatherclothes-66103",
    storageBucket: "weatherclothes-66103.appspot.com",
    messagingSenderId: "754530863180",
    appId: "1:754530863180:web:423b081faa2e7fbd4d8ce9",
    measurementId: "G-J5GBYEKKCQ"
};
  
  // Initialize Firebase
  const firebaseApp = firebase.initializeApp(firebaseConfig);
  firebase.analytics();
  const db = firebaseApp.firestore();
  const auth = firebase.auth();
  const provider = new firebase.auth.GoogleAuthProvider();
  const storage = firebase.storage()

  export {auth, provider};
  export default db;
  export {storage, firebase};