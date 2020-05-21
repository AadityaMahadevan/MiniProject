from google.cloud import storage
#from firebase import firebase

#firebase = firebase.FirebaseApplication('')
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import zipfile

# Use a service account
cred = credentials.Certificate('gans-f33bf-firebase-adminsdk-3gmiu-7bb6705f95.json')
firebase_admin.initialize_app(cred)
"""
db = firestore.client()

users_ref = db.collection(u'models')
docs = users_ref.stream()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
"""

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "gans-f33bf-firebase-adminsdk-3gmiu-7bb6705f95.json"


bucket_name = 'gans-f33bf.appspot.com'
#storage_client = storage.Client()
#buckets = storage_client.get_bucket('gans-f33bf.appspot.com')
#print(buckets)
def list_buckets():
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        print(bucket.name)

def download_pretrained_ckpt(bucket_n, model_name):
	
	# bucket_name = "your-bucket-name"
	# source_blob_name = "storage-object-name"
	#Pretrained Models CKPTS/"+model_name+"/"+model_name+"__pretrained_model_ckpt
	src =destination_file_name = "Pretrained Models CKPTS/"+model_name+"/"+model_name+"_pretrained_model.zip"
	storage_client = storage.Client()
	print(src)
	destination = "Pretrained Models CKPTS/"+model_name+ "/"
	
	bucket = storage_client.bucket(bucket_n)
	blob = bucket.blob(src)

	
	print("?!!!ABC")
	if not os.path.exists(destination):
		os.mkdir("Pretrained Models CKPTS")
		os.mkdir("Pretrained Models CKPTS/"+model_name+"/")
	blob.download_to_filename(src)

	print(
	    "Blob {} downloaded to {}.".format(
	        model_name, destination_file_name
	    )
	)

	
	zipfile.ZipFile(destination_file_name, 'r').extractall(destination)

	if os.path.exists(destination_file_name):
		os.remove(destination_file_name)
		print("The file has been deleted!")


#download_pretrained_ckpt(bucket_name,"handwritten_gans")





	


def upload_pretrained_ckpt(bucket_n, source_file_name, destination_blob_name ,model_name):
	zipfile_n=model_name+".zip"
	zf = zipfile.ZipFile(zipfile_n, "w")
	for dirname, subdirs, files in os.walk(source_file_name):
		zf.write(dirname)
	for filename in files:
		zf.write(os.path.join(dirname, filename))
	zf.close()
	"""Uploads a file to the bucket."""
	# bucket_name = "your-bucket-name"
	# zipfile_n = "file.zip"
	# destination_blob_name = "storage-object-name"
	storage_client = storage.Client()
	bucket = storage_client.bucket(bucket_n)
	blob = bucket.blob(destination_blob_name+model_name+"/"+model_name+"_pretrained_model.zip")

	blob.upload_from_filename(zipfile_n)

	print("File {} uploaded to {}.".format(zipfile_n, destination_blob_name))
	if os.path.exists(zipfile_n):
		os.remove(zipfile_n)
		print("The file deleted")

upload_pretrained_ckpt(bucket_name,"handwritten_gans_pretrained_model","Pretrained Models CKPTS/","handwritten_gans")




