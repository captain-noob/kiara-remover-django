from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from PIL import Image
import base64
import random
import string
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import sys
import platform


def home(request):
    return render(request,'index.html')

def funname():
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
    name_bytes = name.encode('ascii')
    name = base64.b64encode(name_bytes)
    name = name.decode('ascii')
    name = name.replace("=", "").lower()
    return name

def upload(request):
    if request.method=='POST':
        photo=request.FILES.getlist('file')
        fs = FileSystemStorage()
        ses=[]
        data=[]
        for i in photo:
            img=['jpg','jpeg','png']
            imgmane=i.name
            ext=imgmane.split('.')
            ext=ext[1].lower()

            if ext in img:
                ext=ext
                name= funname()
                name=name+'.'+ext
                save = fs.save(name, i)
                url = fs.url(save)
                paths='/static'+url
                if platform.system() == 'Windows':
                    paths = paths.replace('/', '\\')
                path=sys.path[0]+paths
                print(path)
                foo=Image.open(path)
                # foo.resize((x,y),Image.ANTIALIAS)
                foo.save(path,optimize=True,quality=30)

                with open(path,'rb') as f:
                    my_string = base64.b64encode(f.read()).decode('utf-8')
                    im_dat ='data:image/png;base64,'+my_string

                print(im_dat)


                data.append(im_dat)
                ses.append(url)



        context={'url':ses ,'image':data}
        return render(request, 'index2.html',context)
    else:
        return home(request)