from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Category,Photo
from django.contrib.auth.decorators import login_required
from .forms import CustomerCreationForm
# Create your views here.

def loginUser(request):
    page='login'
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('Gallery')
            
    return render(request,'photos/login_register.html',{'page':page})

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomerCreationForm()

    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('Gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)

@login_required(login_url='login')
def gallery(request):
    user=request.user
    category=request.GET.get('category')
    if category==None:
        photos=Photo.objects.filter(category__user=user)
    else:
        photos=Photo.objects.filter(category__name=category,category__user=user)        

    categories = Category.objects.filter(user=user)
    context = {'categories':categories,'photos':photos}
    return render(request,'photos/index.html', context)

@login_required(login_url='login')
def viewPhoto(request,pk):
    
    photos=Photo.objects.get(id=pk)
    return render(request,'photos/photo.html',{'photos':photos})
@login_required(login_url='login')
def addPhoto(request):
    user=request.user
    
    categories = user.category_set.all()
    
    if request.method=="POST":
        data=request.POST
        image=request.FILES.get('image')
        
        if data['category']!='none':
            category=Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created=Category.objects.get_or_create(user=user,name=data['category_new'])    
        else:
            category= None
            
        photos=Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )    
        
        return redirect('Gallery')
        
    context = {'categories':categories}
    return render(request,'photos/add.html',context)

