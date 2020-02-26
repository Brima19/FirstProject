from django.shortcuts import render, redirect
from .models import *
import bcrypt 
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,"home.html")

def createUser(request):
    print(request.POST)
    validationErrors = User.objects.uservalidation(request.POST)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(name=request.POST['name'], username= request.POST['username'],password= pw_hash)
        request.session['newuserID'] = newUser.id
    return redirect("/mainpage")

def mainpage(request):
    if 'newuserID' not in request.session:
        return redirect ('/')
    logger = User.objects.get(id= request.session['newuserID'])
    context = {
        "logger": logger,
        "alltravels": Travel.objects.all(),
        "mytravels": Travel.objects.filter(planer = logger) | Travel.objects.filter(jointrip = logger),
        "othertravels": Travel.objects.exclude(Q(planer = logger) | Q(jointrip = logger))
    }
    return render(request, "mainpage.html", context)

def login(request):
    usernameCheck = User.objects.filter(username=request.POST['username'])
    if usernameCheck:
            logged_user = usernameCheck[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['newuserID'] = logged_user.id
                return redirect('/mainpage')
    validationErrors = User.objects.loginvalidation(request.POST)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/")
    return redirect("/mainpage")

def travelCreate(request):
    return render(request, "travels.html")

def travelAdd(request):
    print(request.POST)
    validationErrors = Travel.objects.tripvalidation(request.POST)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/travels/add")
    else:
        print(request.POST)
        loggedinuser = User.objects.get(id=request.session['newuserID'])
        newTrip = Travel.objects.create(destination = request.POST ['dest'], description = request.POST["des"], traveldatefrom = request.POST['tdf'], traveldateto = request.POST['tdt'], planer = loggedinuser)
        return redirect("/mainpage")

def joinTrip(request, travelid):
    logger = User.objects.get(id= request.session['newuserID'])
    joiner = Travel.objects.get(id = travelid )
    joiner.jointrip.add(logger)
    return redirect("/mainpage")

def tripDetail(request, travelid):
    context = {
        'trip': Travel.objects.get(id = travelid)
    }
    return render(request, "tripdetail.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')