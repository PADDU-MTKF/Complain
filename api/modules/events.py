import os
from appwrite.query import Query
from .. import data as db
from .crud import *
from .imageDB import deleteImage

EVENT_TBL = os.getenv("EVENT_TBL")


def getAllEvents(page=0):
    data=getAllDoc(EVENT_TBL,page)
    return data


def addEvent(data):
    status,e=addDoc(EVENT_TBL,data)
    return status,e

def deleteEvent(ID,coverImage):
    status,e=deleteImage(coverImage)
    status,e=wipeDoc(EVENT_TBL,"$id",ID)
    return status,e