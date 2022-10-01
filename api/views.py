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

from locos.models import Builder, Person
from .serializers import BuilderSerializer, PersonSerializer

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
curl http://localhost:8000/api/builder/ -H "Authorization: Token 00cee603ce74d1f0c9708500eee814c72215778a"
"""
# class Builders(generics.ListAPIView):
#     queryset = Builder.objects.all()
#     serializer_class = BuilderSerializer
#     # Following will ensure a good error message when the user has not signed in 
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Class Based View from https://www.django-rest-framework.org/tutorial/3-class-based-views/
# Not used at present as does not offer the PUT/update method in the API screen
class Builders(APIView):
    """
    List all builders, or create a new builder.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        builders = Builder.objects.all()
        serializer = BuilderSerializer(builders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BuilderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function Based View approach

@api_view(['GET', 'POST'])
def builders(request):

    if request.method == 'GET':
        builders = Builder.objects.all()
        serializer = BuilderSerializer(builders, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BuilderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def builder(request, pk):

    if request.method == 'GET':
        try:
            builder = Builder.objects.get(pk=pk)
        except Builder.DoesNotExist:
            return Response({'error': 'Builder not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BuilderSerializer(builder)
        return Response(serializer.data)

    if request.method == 'PUT':
        builder = Builder.objects.get(pk=pk)
        serializer = BuilderSerializer(builder, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        post = Builder.objects.get(pk=pk)
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