import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('gans-f33bf-firebase-adminsdk-3gmiu-7bb6705f95.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
ref = db.collection(u'models')


def display_all(reference):
	docs = reference.stream()

	for doc in docs:
		print(u'{} ->{} '.format(doc.id,doc.to_dict()))

display_all(ref)