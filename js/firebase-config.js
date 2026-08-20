import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
import { getStorage } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js";

// ============================================================================
// IMPORTANT: REPLACE THESE WITH YOUR ACTUAL FIREBASE PROJECT CONFIGURATION!
// You can find these in your Firebase Console > Project Settings > General
// ============================================================================
const firebaseConfig = {
  apiKey: "AIzaSyDqAnyzEn01mTArpi6nzE__IXPYQgTSAPk",
  authDomain: "gips-f1d15.firebaseapp.com",
  projectId: "gips-f1d15",
  storageBucket: "gips-f1d15.firebasestorage.app",
  messagingSenderId: "116129811641",
  appId: "1:116129811641:web:ad1ee64393238b20541f68"
};

let app, auth, db, storage;

try {
  // Prevent initialization if keys are obviously fake
  if (firebaseConfig.apiKey === "YOUR_API_KEY") {
    console.warn("⚠️ Firebase is NOT initialized. Please update js/firebase-config.js with your real credentials.");
  } else {
    app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    db = getFirestore(app);
    storage = getStorage(app);
    console.log("Firebase initialized successfully.");
  }
} catch (error) {
  console.error("Firebase initialization error:", error);
}

export { app, auth, db, storage };
