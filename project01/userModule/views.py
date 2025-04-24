from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .serializer import UserModuleSerializer

# Handles /user/ -> GET (all), POST (new user)
@api_view(['GET', 'POST'])
def user_path(request):
    if request.method == 'GET':
        #Get All
        users = Users.objects.all()
        serializer = UserModuleSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        #Save
        serializer = UserModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Handles /user/<userID>/ -> GET, PUT, DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def user_byId_path(request, userID):
    try:
        user = Users.objects.get(pk=userID)
    except Users.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        #Get By Id
        serializer = UserModuleSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        #Update By Id
        serializer = UserModuleSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        #Delete By Id
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
