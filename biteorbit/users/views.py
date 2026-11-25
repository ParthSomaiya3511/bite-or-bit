from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserProfileSerializer
from .models import UserProfile

# =========================
# REGISTER
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):

    try:

        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        # CHECK EMPTY
        if not username or not email or not password:

            return Response({

                "success": False,
                "message": "All fields required"

            })

        # USER EXISTS
        if User.objects.filter(username=username).exists():

            return Response({

                "success": False,
                "message": "Username already exists"

            })

        # EMAIL EXISTS
        if User.objects.filter(email=email).exists():

            return Response({

                "success": False,
                "message": "Email already exists"

            })

        # CREATE USER
        user = User.objects.create_user(

            username=username,
            email=email,
            password=password

        )

        return Response({

            "success": True,
            "message": "Registration Successful"

        })

    except Exception as e:

        return Response({

            "success": False,
            "message": str(e)

        })


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:

        refresh = RefreshToken.for_user(user)

        return Response({

            "success": True,

            "access": str(refresh.access_token),

            "refresh": str(refresh),

            "username": user.username

        })

    return Response({

        "success": False,
        "message": "Invalid username or password"

    })


@api_view(["GET", "PUT"]) 
@permission_classes([IsAuthenticated]) 

def user_profile(request): 
    
    profile, created = UserProfile.objects.get_or_create( 
        user=request.user 
    ) 
    
    # GET PROFILE 
    if request.method == "GET": 
        serializer = UserProfileSerializer(profile) 
        return Response(serializer.data) 
    
    # UPDATE PROFILE 
    serializer = UserProfileSerializer( 
        profile, 
        data=request.data, 
        partial=True 
    ) 
    
    if serializer.is_valid(): 
        serializer.save() 
        
        return Response({ 
            "success": True, 
            "data": serializer.data 
        }) 
    
    return Response(serializer.errors)