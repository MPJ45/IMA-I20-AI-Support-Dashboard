import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase App
if not firebase_admin._apps:
    cred = credentials.Certificate("/home/darkdemon/firebase_project/firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://ima-i20-default-rtdb.firebaseio.com/"
    })

# Function to get database reference
def get_db_ref(path):
    return db.reference(path)
