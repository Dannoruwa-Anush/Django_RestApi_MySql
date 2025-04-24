from django.urls import path
from .views import user_path, user_byId_path

urlpatterns = [
    #url : /user/ part will be added from project01/settings.py

    #url: /user/
    path('', user_path, name='user_path'),                   # Handles GET (all users) and POST (create)
    
    #url: /user/id
    path('<int:userID>/', user_byId_path, name='user_byId_path'),  # Handles GET, PUT, DELETE for specific user
]
