import json
import streamlit as st
from firebase_admin import credentials, db
import firebase_admin

if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["FIREBASE_KEY"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://ima-i20-default-rtdb.firebaseio.com/"
    })

def get_db_ref(path):
    return db.reference(path)
