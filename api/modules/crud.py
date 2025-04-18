
import os
from appwrite.query import Query
from .. import data as db


    
def addDoc(TBL,data):
    status,e=db.addDocument(TBL,data)
    return status,e

def getDoc(TBL,key,value):
    profile=[]
    profile=db.getDocument(TBL,query=[Query.equal(key, [value])])    
    return profile[0] if profile else []

def getAllDoc(TBL,page=0):
    profile=[]
    limit=25
    offest=limit*page
    profile=db.getDocument(TBL,query=[Query.limit(limit),Query.offset(offest),Query.order_desc("$createdAt")])    
    return profile if profile else []

def getDocID(TBL,key,value):
    profile=getDoc(TBL,key,value)
    docID=profile["id"] if profile else ""
    
    if profile and profile["deleted"]:
        docID=""
    return docID
    
def updateDoc(TBL,ID,data):
    value=data[ID]
    docId=getDocID(TBL,ID,value)
    if not docId:
        return False,"Doc Do not exist"
    status,e=db.updateDocument(TBL,docId,data)
    return status,e

def deleteDoc(TBL,ID,value):
    docId=getDocID(TBL,ID,value)
    if not docId:
        return False,"Doc Do not exist"
    status,e=db.updateDocument(TBL,docId)
    return status,e

def wipeDoc(TBL,ID,value):
    docId=getDocID(TBL,ID,value)
    if not docId:
        return False,"Doc Do not exist"
    status,e=db.deleteDocument(TBL,docId)
    return status,e