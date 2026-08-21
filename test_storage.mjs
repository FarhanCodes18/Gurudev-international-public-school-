import { initializeApp } from "firebase/app";
import { getStorage, ref, uploadString } from "firebase/storage";

const firebaseConfig = {
  apiKey: "AIzaSyDh401C4sAgg68T7RsB4XIITzcuEtZo5Kc",
  authDomain: "gips-eeaca.firebaseapp.com",
  databaseURL: "https://gips-eeaca-default-rtdb.firebaseio.com",
  projectId: "gips-eeaca",
  storageBucket: "gips-eeaca.firebasestorage.app",
  messagingSenderId: "73492038814",
  appId: "1:73492038814:web:8790a5bff15cac1189678f"
};

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

const storageRef = ref(storage, 'test_upload.txt');
uploadString(storageRef, 'Hello World', 'raw').then(() => {
    console.log("SUCCESS");
}).catch((error) => {
    console.error("ERROR:", error.message);
});
