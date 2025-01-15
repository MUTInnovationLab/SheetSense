// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, collection, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-storage.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBvLwOd23fTx6RpAuodsyFZwntry6AV9Ik",
  authDomain: "cvsystem-253f9.firebaseapp.com",
  projectId: "cvsystem-253f9",
  storageBucket: "cvsystem-253f9.appspot.com",
  messagingSenderId: "133527156661",
  appId: "1:133527156661:web:8d8794eeae33b16dabcbfc"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);
const db = getFirestore(app);