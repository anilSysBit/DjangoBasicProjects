from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Blog, Category, Review
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# Create your views here.



def sucess_mail():
    subject = 'Your Email Subject'
    from_email = settings.EMAIL_HOST_USER
    to_email = 'haflenhauro808@gmail.com'

    html_content = render_to_string('email/register_sucess.html', {'content': 'value'})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    msg.send()


def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    query = Blog.objects.filter(
        Q(category__name__icontains=q)|
        Q(title__icontains =q) |
        Q(description__icontains = q) |
        Q(user__username__icontains = q)|
        Q(category__name__istartswith=q) |
        Q(title__istartswith=q)
    ).order_by('-created')

    count = query.count()
    category = Category.objects.all()
    context = {'blogs':query,'category':category,'count':count}
    return render(request,'html/homepage.html',context)


def blogpage(request,pk):
    blog = Blog.objects.get(id = pk)

    if request.method == "POST":
        review = Review.objects.create(
        user = request.user,
        blog = blog,
        body = request.POST.get('body')
        )
        review.save()
        return redirect('blogpage',pk=pk)

    review = Review.objects.filter(blog = blog).order_by('-created')

    context = {'blog':blog,'reviews':review}

    return render(request,'html/blogpage.html',context)



def loginpage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error('User Doesnot Exists')

        user = authenticate(request,username=username,password = password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error('Authentiation Crecidentals Doesnot Match Try Again')
    return render(request,'html/loginpage.html',{'page':page})


def logoutUser(request):
    logout(request)
    return redirect('home')


def signup(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            sucess_mail()
            return redirect('home')
        
        else:
            messages.error(request,'An Error Occured During The process')

    context = {'signupForm':form}

    return render(request,'html/loginpage.html',context)



@login_required(login_url='login')
def CreateBlog(request):
    action = 'create'
    user = request.user

    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = Category.objects.get(id = category_id)
        title = request.POST.get('title')
        description = request.POST.get('description')

        blog = Blog.objects.create(
            category=category,
            user = user,
            title = title,
            description = description
        )
        blog.save()
        return redirect('home')
    
    context = {'category':Category.objects.all(),'action':action}

    return render(request,'html/createblog.html',context)



@login_required(login_url='login')
def UpdateBlog(request,pk):
    blog = Blog.objects.get(id = pk)

    if request.user != blog.user:
        messages.error('Not Allowed To Update the Record Choose your own Blog post.')
        return redirect('home')
    
    if request.method == "POST":
        blog.category = Category.objects.get(id=request.POST.get('category'))
        blog.title = request.POST.get('title')
        blog.description = request.POST.get('description')
        blog.save()
        messages.success(request,'Sucessfully Updated your Vaues')
        return redirect('blogpage',pk=pk)
    

    category = Category.objects.all()
    context = {'blog':blog,'category':category}
    return render(request,'html/createblog.html',context)


@login_required(login_url='login')
def deleteBlog(request,pk):

    blog = Blog.objects.get(id = pk)

    if request.user == blog.user:
        blog.delete()
        return redirect('home')
    else:
        messages.error('Not Allowed')
        return redirect('home')
    

    