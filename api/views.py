from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .modules.login import *
from .modules.imageDB import addImage
from .modules.complain import *

from  .modules.utility import checkReq 


# {"username":username, "password":password, "name":name, "phno":phno}

@api_view(['GET'])
def home(request):
    data={"Status": "Ok"}
    return Response(data)




class LoginAPI(APIView):
    
    
    def post(self,request):
        try:
            username,password=request.data["username"],request.data["password"]
            
        except Exception as e:
            return Response({"status":False,"error": f"required: {str(e)}"})
        
        profile,TOKEN=validateUserProfile(username,password)
      
        if profile:
            profile.pop("password",None)
            return Response({"status":True,"result":profile,"TOKEN":TOKEN})
        
        return Response({"status":False,"error": f"Invalid Credentials"})
        
 
class UserAPI(APIView):
    
    def get(self,request,*args, **kwargs):
        TOKEN = request.headers.get('TOKEN')
        
        try:
            username=request.query_params.get("username")
            if not username:
                return Response({"status":False,"error": f"required: username"})
                
        except Exception as e:
            return Response({"status":False,"error": f"required: {str(e)}"})
        
        if not TOKEN:
            return Response({"status":False,"error": f"TOKEN: Login to get data"})
        
        if not validateUserToken(username,TOKEN):
            return Response({"status":False,"error": f"TOKEN: Invalid TOKEN, Login to get data"})
            
            
        result=getUserProfile(username)
        if result:
            result.pop("password",None)
            return Response({"status":True,"result":result})
        
        return Response({"status":False,"error":f"Username not found"})
  
    def post(self,request):
        data=request.data
        try:
            username,password,name,phno=data["username"],data["password"],data["name"],int(data["phno"])
        except Exception as e:
            return Response({"status":False,"error": f"required: {str(e)}"})
        
        status,req=checkReq([username,password,name,phno])
        if not status:
            return Response(req)
        
        data={"username":username,"password":password,"name":name,"phno":phno}
        status,e=createUserProfile(data)
        if not status:
            return Response({"status":False,"error":f"Somthing Went Wrong : {e}"})
  
        return Response({"status":True})
    
    def delete(self,request):
        TOKEN = request.headers.get('TOKEN')
        
        try:
            username=request.data["username"]
        except Exception as e:
            return Response({"status":False,"error": f"required: {str(e)}"})
        
        if not TOKEN:
            return Response({"status":False,"error": f"TOKEN: Login to delete data"})
        
        if not validateUserToken(username,TOKEN):
            return Response({"status":False,"error": f"TOKEN: Invalid TOKEN, Login to delete data"})
        
        status,e=deleteUserProfile(username)
        if not status:
            return Response({"status":False,"error":f"Somthing Went Wrong : {e}"})
  
        return Response({"status":True})
    
    def put(self,request):
        TOKEN = request.headers.get('TOKEN')
        
        data=request.data
        try:
            username,password,name,phno=data["username"],data["password"],data["name"],int(data["phno"])
        except Exception as e:
            return Response({"status":False,"error": f"required: {str(e)}"})
        
        if not TOKEN:
            return Response({"status":False,"error": f"TOKEN: Login to edit data"})
        
        if not validateUserToken(username,TOKEN):
            return Response({"status":False,"error": f"TOKEN: Invalid TOKEN, Login to edit data"})
        
        status,req=checkReq([username,password,name,phno])
        if not status:
            return Response(req)
        
        data={"username":username,"password":password,"name":name,"phno":phno}
        status,e=updateUserProfile(data)
        if not status:
            return Response({"status":False,"error":f"Somthing Went Wrong : {e}"})
  
        return Response({"status":True})
     
     
class ComplainAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self,request,*args, **kwargs):
        try:
            page=int(request.query_params.get("page"))
            if not page:
                page=0
                
        except Exception as e:
            page=0
        
        username=request.query_params.get("username")
        if username:
            data=getUserComplains(page,username)
        else:
            data=getAllComplains(page)
            
        
        if not data:
            return Response({"status":False,"error":f"Somthing Went Wrong"})
  
        return Response({"status":True,"result":data})
            
    def post(self,request):
        
        TOKEN = request.headers.get('TOKEN')
        USERNAME = request.headers.get('USERNAME')
        
        print(TOKEN,USERNAME)
        if not TOKEN or not USERNAME:
            return Response({"status":False,"error": f"TOKEN & USERNAME: Login to add data"})
        
        if not validateUserToken(USERNAME,TOKEN):
            return Response({"status":False,"error": f"TOKEN: Invalid TOKEN, Login to add data"})
        
        data=request.data
        
        
        try:
            title,description,location,image1,image2,image3=data["title"],data["description"],data["location"],request.FILES.get("image1"),request.FILES.get("image2"),request.FILES.get("image3")
        except Exception as e:
            return Response({"status":False,"error": f"required: {str(e)}"})
        
        status,req=checkReq([title,description,location])
        if not status:
            return Response(req)
        
        if not (image1):
            return Response({"status":False,"error": f"required: image1"})

        file_url_1,e=addImage(image1)
        file_url_2=""
        file_url_3=""
        
        if not file_url_1:
            return Response({"status":False,"error": f"Somthing went wrong while file1 upload --> {e}"})
        
        if image2:
             file_url_2,e=addImage(image2)
             if not file_url_2:
                return Response({"status":False,"error": f"Somthing went wrong while file2 upload --> {e}"})
        if image3:
             file_url_3,e=addImage(image3)
             if not file_url_3:
                return Response({"status":False,"error": f"Somthing went wrong while file3 upload --> {e}"})
             
             
       
        
        data={"username":USERNAME, 
              "title":title,
              "description":description,
              "location":location,
              "progress":"Created",
              "image1":file_url_1}

        if file_url_2:
            data["image2"]=file_url_2
        if file_url_3:
            data["image3"]=file_url_3
        
        status,e=addComplain(data)
        if not status:
            return Response({"status":False,"error":f"Somthing Went Wrong : {e}"})
  
        return Response({"status":True})
    
    def delete(self,request):
        
        TOKEN = request.headers.get('TOKEN')
        USERNAME = request.headers.get('USERNAME')
        
        if not TOKEN or not USERNAME:
            return Response({"status":False,"error": f"TOKEN & USERNAME: Login to add data"})
        
        if not validateUserToken(USERNAME,TOKEN):
            return Response({"status":False,"error": f"TOKEN: Invalid TOKEN, Login to add data"})
        
        id=request.data.get("id")
        image1=request.data.get("image1")
        image2=request.data.get("image2")
        image3=request.data.get("image3")
        
        
        if not id or not image1:
            return Response({"status":False,"error": f"ID and image1: Required ID and image1"})
            
        status,e=deleteComplain(id,image1,image2,image3)
        if not status:
            return Response({"status":False,"error":f"Somthing Went Wrong : {e}"})
  
        return Response({"status":True})
    
      
        
           




