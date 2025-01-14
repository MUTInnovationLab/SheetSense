// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD-y5cGo8Da9eFCICNSw8V9O9bZxKGLtg4",
  authDomain: "sheetsensedb.firebaseapp.com",
  projectId: "sheetsensedb",
  storageBucket: "sheetsensedb.firebasestorage.app",
  messagingSenderId: "834503780189",
  appId: "1:834503780189:web:4db6a0c7f0cf486ce02ab4",
  measurementId: "G-6GW7RKRQL4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);