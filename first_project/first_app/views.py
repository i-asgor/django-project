from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from first_app.models import AccessRecord, Topic, Webpages, Users
from first_app.forms import NewUserForm, UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    webpages_list = AccessRecord.objects.order_by('date')
    web_dict = {'access_record':webpages_list}
    return render(request,'first_app/index.html',context=web_dict)

@login_required
def special(request):
    return HttpResponse('You are logged in, Nice!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user(request):
    user_list = Users.objects.order_by('first_name')
    user_dict = {'users':user_list}
    return render(request,'first_app/user.html', context=user_dict)

def NewUserForm(request):
    form = forms.NewUserForm()

    if request.method == 'POST':
        form = forms.NewUserForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print('ERROR FORM INVALID')
    return render(request,'first_app/NewUser.html',{'form':form})

def Form_page_views(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print('validation success')
            print('NAME :' +form.cleaned_data['name'])
            print('EMAIL :' +form.cleaned_data['email'])
            print('TEXT :' +form.cleaned_data['text'])


    return render(request,'first_app/form_page.html',{'form':form})

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'first_app/admin_registration.html',
                                                    {'user_form':user_form,
                                                    'profile_form':profile_form,
                                                    'registered':registered})
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpReponse('Account is not active')
        else:
            print('Someone tries to login and failed')
            print('username: {} and password {}'.format(username,password))
            return HttpResponse('Invalid Username and Password')

    else:
        return render(request,'first_app/login.html',{})            
