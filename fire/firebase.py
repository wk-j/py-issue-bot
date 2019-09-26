import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('.keys/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def insert_firebase(title, description, label):
    doc_ref = db.collection("issues").document()
    doc_ref.set({
        "title": title,
        "description": description,
        "label": label
    })
