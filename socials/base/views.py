import email
from multiprocessing import context
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives,send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic import DetailView,CreateView
from django.contrib.auth.views import PasswordChangeView
from .models import *
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
def home(request):
    context={}
    return render(request,"base/home.html",context)

def profile(request):
    context={}
    return render(request,"base/profile.html",context)
    
# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        login_username=request.POST.get('username', None)
        user_password=request.POST["password"]
        user = authenticate(request,username=login_username, password = user_password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.INFO, 'You have successfully logged in.')
            return redirect('/')

        else:
            messages.add_message(request, messages.INFO, 'Invalid username or password.')
            return render(request,"base/login.html")

    return render(request,"base/login.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST': 
        email=request.POST['email']
        password=request.POST['password']
        username=request.POST['username']
        email=email.rstrip()

        if email == '' or password == '' or username == '':
            messages.error(request,"Please fill all the fields.")
            return render(request,"base/signup.html")
        
        elif User.objects.filter(username=username).exists(): 
            messages.add_message(request, messages.INFO, 'Username already exists.')
            return render(request,"base/signup.html")
        
        elif User.objects.filter(email=email).exists():
            messages.add_message(request, messages.INFO, 'Email already exists.')
            return render(request,"base/signup.html")

        else :
            user = User.objects.create(email=email, username=username, password=make_password(password))
            user.save() 
            auth_login(request, user)    
            messages.add_message(request, messages.INFO, 'You have successfully signed up.')
            return redirect('/')
    else:
        return render(request,"base/signup.html")
    

def logout(request):
    auth_logout(request)
    return redirect('/')

def friends(request):
    context={}
    return render(request,"base/friends.html",context)

def error(request):
    context={}
    return render(request,"base/404.html",context)

def post(request):
    context={}
    return render(request,"base/post.html",context)

def otherprofile(request):
    context={}
    return render(request,"base/Otherprofile.html",context)

class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name='registration/edit_profile_page.html'
    # fields = ['bio','profile_pic','website_url','facebook_url','twitter_url','instagram_url']
    # form_class=EditProfileNewForm
    success_url=reverse_lazy('home')

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self,*args,**kwargs):
        # users=Profile.objects.all()
        context=super(ShowProfilePageView,self).get_context_data(*args,**kwargs)
        page_user=get_object_or_404(Profile,id=self.kwargs['pk'])
        context["page_user"]=page_user
        return context

class PasswordsChangeView(PasswordChangeView):
    #    form_class= PasswordChangingForm
       #form_class= PasswordChangeForm
       success_url= reverse_lazy('password_success')
       #success_url= reverse_lazy('home')

class AddPostView(CreateView):
    model = Post
    # form_class = PostForm
    template_name = 'add_post.html'

class AddCommentView(CreateView):
    # model = Comment
    # form_class = CommentForm
    template_name = 'base/add_comment.html'

    def form_valid(self,form):
        form.instance.post_id=self.kwargs['pk']
        return super().form_valid(form)

class UpdatePostView(UpdateView):
    model = Post
    # form_class=EditForm
    template_name = 'update_post.html'
    # fields = ['title','title_tag','body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


