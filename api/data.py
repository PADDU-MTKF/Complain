from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from appwrite.id import ID
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile


import os


try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass



# STORAGE_URL=f"https://cloud.appwrite.io/v1/storage/buckets/{os.getenv("STORAGE_ID")}/files/{FILE_ID}/view?project={os.getenv("PROJECT_ID")}"

client = Client()

DB_ID=os.getenv('DB_ID')
STORAGE_ID=os.getenv('STORAGE_ID')
PROJECT_ID=os.getenv('PROJECT_ID')
ENDPOINT= "https://appdb.lazythinkers.in/v1"
# ENDPOINT= "https://cloud.appwrite.io/v1"


(client
 # Setting API Endpoint
 .set_endpoint(ENDPOINT)
 # Setting Project ID
 .set_project(PROJECT_ID)
 # Setting API Key 
 .set_key(os.getenv('API_KEY'))
 )

databases = Databases(client)
storage = Storage(client)







def getAttribute(collection_id):
    result = databases.list_attributes(DB_ID,collection_id)
    attribute=result['attributes']
    
    att_lists=[]
    
    for each_attribute in attribute :
        
        name=each_attribute["key"]
        type=each_attribute["type"]
        required=each_attribute["required"]
        default=each_attribute["default"]
        # print(each_attribute)
        size=each_attribute["size"] if "size" in each_attribute else 0
     
        dics={"column_name":name,"column_type":type,"required":required,"default":default,"size":size} 
       
        att_lists.append(dics)
        
    return att_lists
    
# print(getAttribute(db_id,collection_id))
def getDocument(collection_id,query=None):
    result = databases.list_documents(DB_ID, collection_id,query)
    document=result['documents']
    # print(document)
    
    doc_list=[]
    attr_lists=getAttribute(collection_id)

    for each_document in document:
        doc_id=each_document['$id']
        dic={}
        dic['id']=doc_id
        
        for each in attr_lists:
            column_name=each["column_name"]
            if each['column_type']=="datetime" and each_document[column_name] is not None:
                value=each_document[column_name].split("T")[0]
            else:
                value=each_document[column_name]
                
            dic[column_name.replace("_"," ")]=value
        doc_list.append(dic)
        
    return doc_list


def deleteDocument(collection_id,document_id):
    try:
        databases.delete_document(DB_ID, collection_id,document_id)
        return True,""
    except Exception as e:
        print("Error deleting document : ",e)
        return False,str(e)


def addDocument(collection_id,data):
    try:
        databases.create_document(DB_ID,collection_id, ID.unique(), data)
        return True,""
    except Exception as e:
        print("Error adding document : ",e)
        return False,str(e)
    
# deleteDocument("65e2d807b75e8ade83aa","65e2fd824f5c44283c76","65e5756c9255fd882005")

def updateDocument(collection_id,document_id,data):
    try:
        databases.update_document(DB_ID, collection_id, document_id,data)
        return True,""
    except Exception as e:
        print("Error Editing document : ",e)
        return False,str(e)


def addStorage(file,name):
    try:
    
        file.seek(0)
        c=file.read()
        
        
        file_info = storage.create_file(STORAGE_ID,ID.unique(),InputFile.from_bytes(c,name))
        
        
        url=f"{ENDPOINT}/storage/buckets/{STORAGE_ID}/files/{file_info['$id']}/view?project={PROJECT_ID}"
        
        return url,""
    except Exception as e:
        return None,e


def deleteStorage(file_url):
    try:
        file_id=file_url.replace(f"{ENDPOINT}/storage/buckets/{STORAGE_ID}/files/","").replace(f"/view?project={PROJECT_ID}","")
        storage.delete_file(STORAGE_ID, file_id)   
        return True,""
    except Exception as e:
        return False,e


