from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from locos.models import Builder
from .serializers import BuilderSerializer

class BuilderList(generics.ListAPIView):
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializer
    # Following will ensure a good error message when the user has not signed in 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

"""
Authentication code based on 
Course https://www.packtpub.com/product/creating-apis-with-python-django-rest-framework/9781801815390
Code  https://github.com/PacktPublishing/Creating-APIs-with-Python---Django-REST-Framework

Token Based Authentication:-

In settings.py:-

REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication', #To enforce token based authentication
        'rest_framework.authentication.SessionAuthentication']}, #Needed if browser sessions also used in parallel to token based authenticatio

At the command prompt:-

n.b.FOR WINDOWS SYSTEMS, DOUBLE QUOTES ARE USED IN THE FOLLOWING, WHICH HAVE TO BE ESCAPED FOR THE DICTIONARY ENTRIES.

To signup for the first time and obtain a token:-
curl -X POST http://localhost:8000/api/signup/ -H "content-type: application/json" -d "{\"username\":\"paulf2\", \"password\":\"passwordhere\"}"

For a userid with no or a forgotten token id:-
curl -X POST http://localhost:8000/api/login/ -H "content-type: application/json" -d "{\"username\":\"paulf2\", \"password\":\"passwordhere\"}"

To then make a token based API call:-
curl http://localhost:8000/api/builder/ -H "Authorization: Token 081dc56dec9b21bf6d93ad54e1a66843dd405c90"
"""

@csrf_exempt
def signup(request):

  if request.method == 'POST':
    try:
        data = JSONParser().parse(request)
        user = User.objects.create_user(data['username'], password=data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return JsonResponse({'token':str(token)}, status=201)
    except:
        return JsonResponse({'error':'User name taken; please try another one'}, status=400)


@csrf_exempt
def login(request):

  if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error':'Could not login. Please check username and password'}, status=400)
        else:
            try:
              token = Token.objects.get(user=user) 
            except:
              token = Token.objects.create(user=user)                 
            return JsonResponse({'token':str(token)}, status=200)