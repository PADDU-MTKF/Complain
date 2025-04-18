
import os
from appwrite.query import Query
from .. import data as db

from .utility import generate_token,cacheData,isCache


USERS_TBL = os.getenv("USERS_TBL")




def createUserProfile(data):
    status,e=db.addDocument(USERS_TBL,data)
    return status,e

def getUserProfile(username):
    profile=[]
    profile=db.getDocument(USERS_TBL,query=[Query.equal("username", [username])])    
    return profile[0] if profile else []

def getUserDocID(username):
    profile=getUserProfile(username)
    docID=profile["id"] if profile else ""
    
    if profile and profile["deleted"]:
        docID=""
    return docID
    
def updateUserProfile(data):
    username=data["username"]
    docId=getUserDocID(username)
    if not docId:
        return False,"User Do not exist"
    status,e=db.updateDocument(USERS_TBL,docId,data)
    return status,e

def deleteUserProfile(username):
    docId=getUserDocID(username)
    if not docId:
        return False,"User Do not exist"
    status,e=db.updateDocument(USERS_TBL,docId,{"deleted":True})
    return status,e

def validateUserProfile(username,password):
    profile=db.getDocument(USERS_TBL,query=[Query.equal("username", [username]),Query.equal("password", [password]),Query.equal("deleted", [False])])   
    
    if profile:
        Token=generate_token()
        cacheData(username,Token)
        return profile[0],Token 
    
    return False,""

def validateUserToken(username,Token):
    status,value=isCache(username)
    if status and Token==value:
        return True
    return False