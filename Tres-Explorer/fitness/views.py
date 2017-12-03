from django.shortcuts import render_to_response, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate




### HOME

def home(request):

	context = RequestContext(request, {'user': request.user})
	return render_to_response('home.html', context_instance=context)




### USER SIGNUP AND SIGNIN AND FBSIGNIN OLD 

def isExists(request,name):
	user = ''
	try:
		user = User.objects.get(username=name)
	except User.DoesNotExist:
		return False
	return True

def addUser(request,name,pwd):
    newUser=User(username=name)
    newUser.set_password(pwd)
    newUser.save()

    theUser=User.objects.get(username=name)
    if not theUser:
        id="failure"
    else:
        id=theUser.id
    return id

@csrf_exempt
def signup(request):
	
    if request.method == "POST":
        ajaxData = json.loads(str(request.body))
        username = ajaxData["username"]
        pwd = ajaxData["pwd"]
        if isExists(request,username) is False:
            newID = addUser(request,username,pwd)
        else:
            return HttpResponse("existUserName")

        return HttpResponse(newID)
    else:
        return HttpResponse("error")

def usersignin(request,name,pwd):
    try:
        theUser=authenticate(username=name,password=pwd)
    except User.DoesNotExist:
        return "failure"
    else:
    	if theUser:
        	return theUser.id
        else:
        	return "failure"

@csrf_exempt
def signin(request):
	response = {}
	if request.method == "POST":
		ajaxData = json.loads(str(request.body))
		username = ajaxData["username"]
		pwd = ajaxData["pwd"]
		uid=usersignin(request,username,pwd)
		response = HttpResponse(uid)
	else:
		response = HttpResponse("error")



	return response

@csrf_exempt
def fb_signin(request):
    response = {}
    if request.method == "POST":
        ajaxData = json.loads(str(request.body))
        fbid = ajaxData["fbid"]
        email = ajaxData["email"]
        user = User.objects.get(email=email)
        uid=usersignin(request,email,user.pwd)
        response = HttpResponse(uid)
    else:
        response = HttpResponse("error")



	return response

