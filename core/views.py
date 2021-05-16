from django.shortcuts import render
from django.conf import settings

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, GlobalDatabaseSerializer
from .models import User, GlobalDatabase
from .tokenService import TokenAuthentication, generate_token

# Create your views here.

def home(request):
    res = {
        'Register' : '/register',
        'Sign in' : '/signin',
        'Mark Spam' : '/markSpam',
        'Search by Name' : 'search/name',
        'Search by Phone' : 'search/phone',
        'Detail Search' : 'search/detail',
    }

    return Response(res, status = status.HTTP_200_OK)

# ------------------------------------------------------------------------------------

# Registering our new user
# Accepts name, phone, password and email(optional) as payload

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

# ------------------------------------------------------------------------------------

# Obtaining auth token
# Accepts phone and password as payload

@api_view(['POST',])
def signin(request):
    phone = request.data.get('phone')
    password = request.data.get('password')

    try:
        # checking if the user is registered
        user = User.objects.get(phone = phone)

        if user.check_password(password):
            token = generate_token(user)

            return Response(
                {
                    'token': token.key
                },
                status = status.HTTP_201_CREATED
            )

        else:
            res = {
                'Password error' : 'Please enter the correct password'
            }
            return Response(res, status = status.HTTP_403_FORBIDDEN)

    except Exception as e:
        res = {
            'Value Error' : 'No user with the provided credentials'
        }
        # print(str(e))
        return Response(res, status = status.HTTP_404_NOT_FOUND)

# ------------------------------------------------------------------------------------

# MARK SPAM 
# Accepts phone as payload

@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def markSpam(request):
    phone = request.data.get('phone')

    try:
        users = GlobalDatabase.objects.filter(phone = phone) # Searching all occurances of the number

        for user in users: # marking all occurances of the number as spam
            user.spam_status = True
            user.save()

        res = {
            'Marked Successfully' : 'Person marked as spam.'
        }
        return Response(res, status = status.HTTP_200_OK)

    except Exception as e:
        res = {
            'Value Error' : 'No person with the provided credentials'
        }
        # print(str(e))
        return Response(res, status = status.HTTP_404_NOT_FOUND)


# -----------------------------------------------------------------------------------------

# SEARCH BY NAME
# Accepts name as payload

@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def searchName(request):
    name = request.data.get('name')

    first = GlobalDatabase.objects.filter(name__startswith = name) # 'name' in starting
    second = GlobalDatabase.objects.filter(name__icontains = name).exclude(name__startswith = name) # contains 'name' but not in start

    first_serializer = GlobalDatabaseSerializer(first, many = True)
    second_serializer = GlobalDatabaseSerializer(second, many = True)

    return Response(first_serializer.data + second_serializer.data , status = status.HTTP_200_OK)

# -----------------------------------------------------------------------------------------

# SEARCH BY PHONE
# Accepts phone as payload

@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def searchPhone(request):
    phone = request.data.get('phone')

    try:
        obj = GlobalDatabase.objects.get(phone = phone, registration_status = True) # if gets a registered user
        serializer = GlobalDatabaseSerializer(obj)

    except:
        obj = GlobalDatabase.objects.filter(phone = phone) # otherwise
        serializer = GlobalDatabaseSerializer(obj, many = True)

    return Response(serializer.data, status = status.HTTP_200_OK)


# -----------------------------------------------------------------------------------------

# Detail Search
# Accepts 'id' of GlobalDatabase's object instance as payload

@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def searchDetail(request):
    id = request.data.get('id')

    try:
        obj = GlobalDatabase.objects.get(id = id) # retrieving id when the user selects a certain field ( from Global Database model)
        
        #general response ( without email )
        res = {
            'name' : obj.name,
            'phone' : obj.phone,
            'spam_status' : obj.spam_status
        }

        if obj.registration_status == True:
            
            # fetching the searched user details from the User model
            searched_user = User.objects.get(phone = obj.phone)

            # fetching contacts list of the searched_user
            contacts_list = GlobalDatabase.objects.filter(user = searched_user)

            for contact in contacts_list:
                if contact.phone == request.user.phone: # checking if the requested user is in the searched user's contact list
                    flag = True
                    break
                else:
                    flag = False

            if flag:
                res = {
                    'name' : obj.name,
                    'email' : obj.email, # sending email as response if all the conditions are fulfilled
                    'phone' : obj.phone,
                    'spam_status' : obj.spam_status
                }

        return Response(res, status = status.HTTP_200_OK)

    except Exception as e:
        res = {
            'Value Error' : 'No person with the provided id.'
        }
        # print(str(e))
        return Response(res, status = status.HTTP_404_NOT_FOUND)


##############################################################################################

