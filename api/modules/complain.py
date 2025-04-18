import os
from appwrite.query import Query
from .. import data as db
from .crud import *
from .imageDB import deleteImage

COMPLAIN_TBL = os.getenv("COMPLAIN_TBL")


def getAllComplains(page=0):
    data=getAllDoc(COMPLAIN_TBL,page)
    return data

def getUserComplains(page=0,username=None):
    data=getAllDoc(COMPLAIN_TBL,page,username)
    return data


def addComplain(data):
    status,e=addDoc(COMPLAIN_TBL,data)
    return status,e

def deleteComplain(ID,image1,image2="",image3=""):
    status,e=deleteImage(image1)
    if image2:
        status,e=deleteImage(image2)
    if image3:
        status,e=deleteImage(image3)
        
    status,e=wipeDoc(COMPLAIN_TBL,"$id",ID)
    return status,e