// Import Firebase functions
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-storage.js";
import { getFirestore, collection, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// Firebase configuration
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

// Function to format date for document ID (date only)
function formatDateForId() {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
}

// Function to handle file upload to Firebase Storage
async function uploadFileToStorage(file, collectionName) {
    try {
        const timestamp = Date.now();
        const fileName = `${collectionName}/${timestamp}_${file.name}`;
        const storageRef = ref(storage, fileName);
        
        const snapshot = await uploadBytes(storageRef, file);
        const downloadURL = await getDownloadURL(snapshot.ref);
        
        return {
            fileName: file.name,
            uploadPath: fileName,
            downloadURL: downloadURL,
            timestamp: timestamp,
            fileType: file.type,
            fileSize: file.size
        };
    } catch (error) {
        console.error("Error uploading file:", error);
        throw error;
    }
}

// Function to save or update file metadata to Firestore with date-based document ID
async function saveFileMetadata(fileData, collectionName) {
    try {
        const docId = formatDateForId();
        const docRef = doc(db, collectionName, docId);
        
        const docSnap = await getDoc(docRef);
        
        if (docSnap.exists()) {
            const existingData = docSnap.data();
            const files = existingData.files || [];
            files.push({
                fileName: fileData.fileName,
                uploadPath: fileData.uploadPath,
                downloadURL: fileData.downloadURL,
                uploadedAt: new Date(fileData.timestamp),
                fileType: fileData.fileType,
                fileSize: fileData.fileSize
            });
            
            await setDoc(docRef, { files: files }, { merge: true });
        } else {
            await setDoc(docRef, {
                files: [fileData]
            });
        }
        
        return docId;
    } catch (error) {
        console.error("Error saving metadata:", error);
        throw error;
    }
}

// Generic function to handle file uploads
async function handleFileUpload(event, inputId, collectionName, buttonText) {
    event.preventDefault();
    
    const fileInput = document.getElementById(inputId);
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file first');
        return;
    }
    
    const validTypes = [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ];
    
    if (!validTypes.includes(file.type)) {
        alert('Please upload only Excel files (.xls or .xlsx)');
        return;
    }
    
    try {
        const submitButton = event.target.querySelector('button');
        submitButton.disabled = true;
        submitButton.textContent = 'Uploading...';
        
        const fileData = await uploadFileToStorage(file, collectionName);
        await saveFileMetadata(fileData, collectionName);
        
        event.target.reset();
        alert(`${collectionName} file uploaded successfully!`);
    } catch (error) {
        alert('Error uploading file: ' + error.message);
    } finally {
        const submitButton = event.target.querySelector('button');
        submitButton.disabled = false;
        submitButton.textContent = buttonText;
    }
}

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const studentFileForm = document.querySelector('form[action="/upload_student_file"]');
    const weeklyFileForm = document.querySelector('form[action="/upload_Weekly_file"]');
    const monthlyFileForm = document.querySelector('form[action="/upload_Monthly_file"]');
    
    if (studentFileForm) {
        studentFileForm.addEventListener('submit', (e) => 
            handleFileUpload(e, 'student_file', 'students', 'Upload Student File')
        );
    }
    
    if (weeklyFileForm) {
        weeklyFileForm.addEventListener('submit', (e) => 
            handleFileUpload(e, 'weekly_file', 'weekly', 'Upload Report File')
        );
    }

    if (monthlyFileForm) {
        monthlyFileForm.addEventListener('submit', (e) => 
            handleFileUpload(e, 'monthly_file', 'monthly', 'Upload Report File')
        );
    }
});
