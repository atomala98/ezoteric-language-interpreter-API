from django.contrib.auth.models import User

# Create your views here.
from .models import BefungeProgram, BrainfuckProgram, WhitespaceProgram
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BefungeInputSerializer, BefungeSerializer, BrainfuckInputSerializer, BrainfuckSerializer, UserSerializer, RegisterSerializer, WhitespaceInputSerializer, WhitespaceSerializer


@api_view(['GET', 'POST'])
def user_endpoint_list(request):

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
def user_endpoint_detail(request, pk):

    try:
        user = User.objects.get(pk=pk)
    except BrainfuckProgram.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# BRAINFUCK

@api_view(['GET', 'POST', 'DELETE'])
def brainfuck_endpoint_list(request):

    if request.method == 'GET':
        program_instances = BrainfuckProgram.objects.all()
        serializer = BrainfuckSerializer(program_instances, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BrainfuckSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    elif request.method == 'DELETE':
        program_instances = BrainfuckProgram.objects.all()
        program_instances.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'PUT', 'DELETE'])
def brainfuck_endpoint_detail(request, pk):

    try:
        program_instance = BrainfuckProgram.objects.get(pk=pk)
    except BrainfuckProgram.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = BrainfuckSerializer(program_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BrainfuckInputSerializer(program_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        program_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# BEFUNGE


@api_view(['GET', 'POST', 'DELETE'])
def befunge_endpoint_list(request):

    if request.method == 'GET':
        program_instances = BefungeProgram.objects.all()
        serializer = BefungeSerializer(program_instances, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BefungeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        program_instances = BefungeProgram.objects.all()
        program_instances.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'PUT', 'DELETE'])
def befunge_endpoint_detailed(request, pk):

    try:
        program_instance = BefungeProgram.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = BefungeSerializer(program_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BefungeInputSerializer(program_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        program_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST', 'DELETE'])
def whitespace_endpoint_list(request):

    if request.method == 'GET':
        program_instances = WhitespaceProgram.objects.all()
        serializer = WhitespaceSerializer(program_instances, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WhitespaceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        program_instances = WhitespaceProgram.objects.all()
        program_instances.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'PUT', 'DELETE'])
def whitespace_endpoint_detailed(request, pk):

    try:
        program_instance = WhitespaceProgram.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = WhitespaceSerializer(program_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WhitespaceInputSerializer(program_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        program_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    