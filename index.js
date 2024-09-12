// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";


// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBz59MD0xmXBlI5-2Cu0zGaDcGwJqsux38",
  authDomain: "machineheads-1.firebaseapp.com",
  projectId: "machineheads-1",
  storageBucket: "machineheads-1.appspot.com",
  messagingSenderId: "108937002849",
  appId: "1:108937002849:web:f5e43597cb7d23376dcf20",
  measurementId: "G-SHV4HF3EGH"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);