import cloudinary
import cloudinary.uploader
import cloudinary.api
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage

import os
import zipfile

class Model(object):
    cred = credentials.Certificate('gans-f33bf-firebase-adminsdk-3gmiu-7bb6705f95.json')
    firebase_admin.initialize_app(cred)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "gans-f33bf-firebase-adminsdk-3gmiu-7bb6705f95.json"
    bucket_n = 'gans-f33bf.appspot.com'
    url = 'https://res.cloudinary.com/dab45s7en/image/upload/v1586353552/'


    db = firestore.client()
    ref = db.collection(u'models')
    def __init__(self,iid:str,name:str='', details:str='', more_details:str='', images_b:bool=False, pretrained_model_b:bool=False,model_architecture_b:bool=False,images:list=[],pretrained_model:dict={},model_architecture:dict={}):
        self.id = iid
        self.name = name
        self.details = details
        self.more_details = more_details
        self.images_b = images_b
        self.pretrained_model_b = pretrained_model_b
        self.model_architecture_b = model_architecture_b
        self.images = images
        self.pretrained_model = pretrained_model
        self.model_architecture = model_architecture

    def from_dict(self,source):
        self.name = source['name']
        self.details = source['details']
        self.more_details = source['more_details']
        self.images_b = source['images_b']
        self.pretrained_model_b = source['pretrained_model_b']
        self.model_architecture_b = source['model_architecture_b']
        self.images = source['images']
        self.pretrained_model = source['pretrained_model']
        self.model_architecture = source['model_architecture']

    def to_dictt(self):
        data = {
            u'name' : self.name,
            u'details' : self.details,
            u'more_details' : self.more_details,
            u'images_b' : self.images_b,
            u'pretrained_model_b' : self.pretrained_model_b,
            u'model_architecture_b' : self.model_architecture_b,
            u'images' : self.images,
            u'pretrained_model' : self.pretrained_model,
            u'model_architecture' : self.model_architecture
        }
        return data

    def __str__(self):
        return ('id : ' + self.id+'\nname : ' + self.name  + '\ndetails : ' + self.details+'\nmore_details : ' + self.more_details+ '\nimages_b : '+ str(self.images_b)+'\npretrained_model_b : ' + str(self.pretrained_model_b)+'\nmodel_architecture_b : ' + str(self.model_architecture_b)+'\nimages : ' + ','.join(map(str,self.images))+ '\npretrained_model : ' +str(self.pretrained_model)+'\nmodel_architecture : ' +str(self.model_architecture))


    def load_id(self):
        docs = self.ref.document(self.id).get() 
        self.from_dict(docs.to_dict())

    def upload_image(self,args:list):
        try:
            for img in args:
                if os.path.exists(img):
                    ext = os.path.splitext(img)
                    filename = ext[0].rsplit('/',1)[1] 
                    cloudinary.config( 
                      cloud_name = "dab45s7en", 
                      api_key = "438279973731312", 
                      api_secret = "a1Q21X9NKKX3tsyjdZxzR-FbHLU" 
                    )

                    cloudinary.uploader.upload(img,folder =self.id+"/",use_filename= 1, unique_filename = False,public_id =filename)
                    self.images.append(self.url+self.id+"/"+filename+ext[1])
                    self.images_b=True
                    self.update_db
            return True        
                
        except Exception as e:
            print(e)
            return False


    def load_images(self):
        return self.images

    def load_images_refresh(self):
        refresh_my_obj(self)
        return self.images

    def get_images(self):
        return self.images     

    def upload_pretrained_ckpt(self, source_file_name:str,name:str):
        try:
            zipfile_n=self.id+".zip"
            zf = zipfile.ZipFile(zipfile_n, "w")
            for dirname, subdirs, files in os.walk(source_file_name):
                zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
            zf.close()
            """Uploads a file to the bucket."""
            # bucket_name = "your-bucket-name"
            # zipfile_n = "file.zip"

            destination_blob_name = "Pretrained_Models_CKPTS/" + self.id+"/" +name+"/"

            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket_n)
            blob = bucket.blob(destination_blob_name+self.id+"_pretrained_model.zip")
            print("zip created")

            blob.upload_from_filename(zipfile_n)

            print("File {} uploaded to {}.".format(zipfile_n, destination_blob_name))
            if os.path.exists(zipfile_n):
                os.remove(zipfile_n)
                print("The file deleted")

            self.pretrained_model_b = True
            self.pretrained_model.update({name : destination_blob_name+self.id+"_pretrained_model.zip"})
            self.update_db()
            return True
                
        except Exception as e:
            print(e)
            return False

    def set_db(self):
        self.ref.document(self.id).set(self.to_dict())

    def download_pretrained_ckpt(self,model_name):    
        # bucket_name = "your-bucket-name"
        # source_blob_name = "storage-object-name"
        #Pretrained Models CKPTS/"+model_name+"/"+model_name+"__pretrained_model_ckpt
        try:
            main_folder ="Pretrained_Models_CKPTS/" +self.id+"/"+model_name+"/"
            extension = "_pretrained_model.zip"
            src =destination_file_name = main_folder+self.id+"_pretrained_model.zip"
            storage_client = storage.Client()
            print(src)
            destination = main_folder+self.id+"/"
            
            bucket = storage_client.bucket(self.bucket_n)
            blob = bucket.blob(src)

            print("?!!!ABC")
            if not os.path.exists(main_folder): #creating path
                if not os.path.exists("Pretrained_Models_CKPTS/" +self.id+"/"):
                    if not os.path.exists("Pretrained_Models_CKPTS/"):
                        os.mkdir("Pretrained_Models_CKPTS/")
                    os.mkdir("Pretrained_Models_CKPTS/" +self.id+"/")
                os.mkdir(main_folder)
            blob.download_to_filename(src)

            print("Blob {} downloaded to {}.".format(model_name, destination_file_name))
            
            zipfile.ZipFile(destination_file_name, 'r').extractall(destination)

            if os.path.exists(destination_file_name):
                os.remove(destination_file_name)
                print("The file has been deleted!")
            return True
                    
        except Exception as e:
            print(e)
            return False

    def get_list_pretrained_ckpt(self):
        return self.pretrained_model

    def get_list_model_architecture(self):
        return self.model_architecture

    def download_specific_model_architecture(self,m_name:str):
        result = self.get_list_model_architecture()
        model_name = ''
        if result:
            print(result)
            while not model_name in result.keys():
                model_name = m_name   #onclick listener here
            return self.download_model_architecture(model_name)
        return False

    def download_specific_pretrained_ckpt(self,m_name:str):
        result = self.get_list_pretrained_ckpt()
        model_name = ''
        if result:
            print(result)
            while not model_name in result.keys():
                model_name = m_name  #onclick listener here
            return self.download_pretrained_ckpt(model_name)
        return False

    def upload_model_architecture(self,source_file_name,name:str):
        try:
            zipfile_n=self.id+".zip"
            zf = zipfile.ZipFile(zipfile_n, "w")
            for dirname, subdirs, files in os.walk(source_file_name):
                zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
            zf.close()
            """Uploads a file to the bucket."""
            # bucket_name = "your-bucket-name"
            # zipfile_n = "file.zip"
            destination_blob_name = "Model_Architecture/" + self.id+"/" +name+"/"
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket_n)
            blob = bucket.blob(destination_blob_name+self.id+"_model_arch.zip")

            blob.upload_from_filename(zipfile_n)

            print("File {} uploaded to {}.".format(zipfile_n, destination_blob_name))
            if os.path.exists(zipfile_n):
                os.remove(zipfile_n)
                print("The file deleted")
            self.model_architecture_b = True
            self.model_architecture.update({name : destination_blob_name+self.id+"_model_arch.zip"})
            self.update_db()
            return True
        except Exception as e:
            print(e)
            return False
        

        self.model_architecture_b = True
        self.model_architecture.update({name :destination_blob_name+self.id+"_model_arch.zip"})
        self.update_db()

    def download_model_architecture(self,model_name):    
        # bucket_name = "your-bucket-name"
        # source_blob_name = "storage-object-name"
        #Pretrained Models CKPTS/"+model_name+"/"+model_name+"__pretrained_model_ckpt
        try:
            main_folder = "Model_Architecture/" +self.id+"/"+model_name +"/"
            extension = "_model_arch.zip"
            src =destination_file_name = main_folder+self.id+extension
            storage_client = storage.Client()
            print(src)
            destination =main_folder +self.id+"/"

            bucket = storage_client.bucket(self.bucket_n)
            blob = bucket.blob(src)

            if not os.path.exists(main_folder): #creating path
                if not os.path.exists("Model_Architecture/" +self.id+"/"):
                    if not os.path.exists("Model_Architecture/"):
                        os.mkdir("Model_Architecture/")
                    os.mkdir("Model_Architecture/" +self.id+"/")
                os.mkdir(main_folder)

            blob.download_to_filename(src) #downloading

            print("Blob {} downloaded to {}.".format(model_name, destination_file_name))

            zipfile.ZipFile(destination_file_name, 'r').extractall(destination) #extracting

            if os.path.exists(destination_file_name):   #deleting
                os.remove(destination_file_name)
                print("The file has been deleted!")
            return True
                    
        except Exception as e:
            print(e)
            return False
    def get_models(self):
        docs = self.ref.stream()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

    def update_db(self):
        self.ref.document(self.id).update(self.to_dictt())


#obj1 = Model('handwritten_digits',"Handwritten Digits", 'Produces natural handwritten digits.',"Generative Adversarial Networks trained on MNIST handwritten dataset.")
#obj1 = Model('handwritten_digits')
#obj1.load_id()
#print(obj1)
#print(obj1.get_list_model_architecture())
#print(obj1.get_list_pretrained_ckpt())
#imgs = ['imgs/123.jpg','imgs/abc.jpg']
#obj1.upload_image(imgs)
#print(obj1.load_images())

#print(obj1)
#print(obj1)
#obj1.set_db()
#obj1.upload_pretrained_ckpt('model_name_pretrained_model','handwritten_digits_45')
#obj1.upload_model_architecture('handwritten_gans_tensorflow',"handwritten_gans")
#obj1.update_db()
#obj1.download_specific_pretrained_ckpt()
#obj1.download_specific_model_architecture()
#print(obj1)

def get_models():
    db = firestore.client()
    ref = db.collection(u'models')
    docs = ref.stream()
    model_d={}
    for doc in docs:
        model_d[doc.to_dict()["name"]] = doc.id
    return model_d
"""def list_pretrained_ckpt_frm_db(self):
        docs = self.ref.where(u'id', u'==', self.id).where(u'pretrained_model_b',u'==',True).stream()
        for doc in docs:
            print(u'{}'.format(doc.to_dict()))

        if len(docs) == 1:
            print(docs[0].pretrained_model.keys())
            return docs[0].pretrained_model
        else 
            print('error')
            return False

   

 def list_model_architecture_frm_db(self):
        docs = self.ref.where(u'id', u'==', self.id).where(u'model_architecture_b',u'==',True).stream()
        for doc in docs:
            print(u'{}'.format(doc.to_dict()))

        if len(docs) == 1:
            print(docs[0].model_architecture.keys())
            return docs[0].model_architecture
        else 
            print('error')
            return False"""
