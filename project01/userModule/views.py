from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Users
from .serializer import UserModuleSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def user_path(request):
    if request.method == 'GET':
        #Get all users
        logger.info("Fetching all users")
        users = Users.objects.all()
        serializer = UserModuleSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #Create a user
        logger.info("Attempting to create a new user")
        try:
            with transaction.atomic():
                serializer = UserModuleSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    user_id = serializer.data.get('id')
                    logger.info("User created successfully with ID: %s", user_id)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                logger.warning("User creation failed due to validation errors")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Exception while creating user: %s", str(e), exc_info=True)
            return Response(
                {'detail': 'An error occurred while creating the user.', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'PUT', 'DELETE'])
def user_byId_path(request, userID):
    try:
        user = Users.objects.get(pk=userID)
        logger.info("User accessed with ID: %s", userID)
    except Users.DoesNotExist:
        logger.warning("User not found with ID: %s", userID)
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        #Get user by ID
        logger.info("Fetching user with ID: %s", userID)
        serializer = UserModuleSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        #Update user by ID
        logger.info("Updating user with ID: %s", userID)
        try:
            with transaction.atomic():
                serializer = UserModuleSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    logger.info("User updated successfully with ID: %s", userID)
                    return Response(serializer.data)
                logger.warning("User update failed for ID: %s", userID)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Exception while updating user ID %s: %s", userID, str(e), exc_info=True)
            return Response(
                {'detail': 'An error occurred while updating the user.', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'DELETE':
        #Delete user by ID
        logger.info("Deleting user with ID: %s", userID)
        user.delete()
        logger.info("User deleted successfully: %s", userID)
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
