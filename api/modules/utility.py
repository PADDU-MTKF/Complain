import secrets
import string

from django.core.cache import cache


def checkReq(data):
    empty=[]
    for each in data:
        if not each:
            empty.append(each)
    if empty:
        return  False,{"required",empty}  
    
    return True,{}


def generate_token(length=20):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(characters) for _ in range(length))

# ---------------------------------------------- CACHING  ---------------------------------

def isCache(key):
    value = cache.get(key)
    return value is not None, value


def cacheData(key, value, timeout=43200):  # 12 hours = 60*60*12 = 43200 seconds
    cache.set(key, value, timeout)
    
#------------------------------------------------------------------------------------------