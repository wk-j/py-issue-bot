import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date
import time

cred = credentials.Certificate('.keys/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def insert_firebase(title, project, label):
    doc_ref = db.collection("issues").document()
    doc_ref.set({
        "date": time.time(),
        "title": title,
        "project": project,
        "label": label
    })
