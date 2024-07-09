from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view # For Function Based Views
from rest_framework.views import APIView # For Class Based Views

from people.models import Person
from companies.models import Manufacturer
from .serializers import ManufacturerSerializer, PersonSerializer

"""
Registers a user for the first time and provides a token. API call:-
curl -X POST http://localhost:8000/api/register/ -H "content-type: application/json" -d "{\"username\":\"paulf2\", \"password\":\"passwordhere\"}"10
"""
@csrf_exempt
def register(request):

  if request.method == 'POST':
    try:
        data = JSONParser().parse(request)
        user = User.objects.create_user(data['username'], password=data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return JsonResponse({'token':str(token)}, status=201)
    except Exception:
        return JsonResponse({'error':'User name taken; please try another one'}, status=400)


"""
For a userid with no or a forgotten token id:-
curl -X POST http://localhost:8000/api/login/ -H "content-type: application/json" -d "{\"username\":\"paulf2\", \"password\":\"passwordhere\"}"
"""
@csrf_exempt
def login(request):

  if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error':'Could not login. Please check username and password'}, status=400)

        try:
            token = Token.objects.get(user=user) 
        except Exception:
            token = Token.objects.create(user=user)                 
        return JsonResponse({'token':str(token)}, status=200)

"""
To make a token based API call:-
curl http://localhost:8000/api/manufacturer/ -H "Authorization: Token 00cee603ce74d1f0c9708500eee814c72215778a"
"""
# class Manufacturers(generics.ListAPIView):
#     queryset = Manufacturer.objects.all()
#     serializer_class = ManufacturerSerializer
#     # Following will ensure a good error message when the user has not signed in 
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Class Based View from https://www.django-rest-framework.org/tutorial/3-class-based-views/
# Not used at present as does not offer the PUT/update method in the API screen
class Manufacturers(APIView):
    """
    List all manufacturers, or create a new manufacturer.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        manufacturers = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ManufacturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function Based View approach

@api_view(['GET', 'POST'])
def manufacturers(request):

    if request.method == 'GET':
        manufacturers = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ManufacturerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def manufacturer(request, pk):

    if request.method == 'GET':
        try:
            manufacturer = Manufacturer.objects.get(pk=pk)
        except Manufacturer.DoesNotExist:
            return Response({'error': 'Manufacturer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ManufacturerSerializer(manufacturer)
        return Response(serializer.data)

    if request.method == 'PUT':
        manufacturer = Manufacturer.objects.get(pk=pk)
        serializer = ManufacturerSerializer(manufacturer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        post = Manufacturer.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def persons(request):

    if request.method == 'GET':
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PersonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)