import os
from django.conf import settings
from django.http import Http404
from django.shortcuts import render , redirect , HttpResponse
from .models import *
# Create your views here.
def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)
    
    categories = Category.objects.all()
    context = {
        'categories':categories ,
        'photos':photos
    }
    return render(request , 'gallery.html',context)

def download(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb') as fh:
            response= HttpResponse(fh.read(),content_type="application/adminupload")
            response['content-disposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise Http404

def viewphoto(request ,id):
    photo = Photo.objects.get(id=id)
    return render(request , 'photo.html',{'photo':photo})

def addphoto(request):
    categories = Category.objects.all()
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get('image')
        
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category , created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category = category ,
            description= data['description'],
            image = image,

        )

        return redirect('gallery')
 

    context = {
        'categories':categories 
    }
    return render(request , 'add.html',context)