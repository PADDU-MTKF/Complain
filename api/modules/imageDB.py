from PIL import Image
import io
import os
from django.core.files.uploadedfile import InMemoryUploadedFile

from .. import data as db


def compress_image(uploaded_file):
    img = Image.open(uploaded_file)
    
    # Compress the image (adjust the quality as needed)
    img = img.convert('RGB')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=20)
    img_io.seek(0)

    # Create a new InMemoryUploadedFile object with the compressed image data
    compressed_file = InMemoryUploadedFile(
        img_io, None, uploaded_file.name, 'image/jpeg', img_io.tell(), None
    )

    return compressed_file

def deleteImage(imageURL):
    status,e=db.deleteStorage(imageURL)
    return status,e


def addImage(uploaded_file):
    imgName=  uploaded_file.name  
    compressed_file = compress_image(uploaded_file)
    
    file_url,e = db.addStorage(
            compressed_file.file,  # file-like object
            imgName  # original file name
        )
    print (file_url)
    return file_url,e