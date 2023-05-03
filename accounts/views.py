import email
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import LoginSerializer, ChangePasswordSerializer, UserRegisterationSerializer, UserDetailSerializer, UserLogoutSerializer, AdminRegistrationSerializer, SuperAdminSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from .helpers.generator import generate_password
from .permissions import IsAdmin, IsSuperUser
User = get_user_model()


class UserRegisterView(APIView):
    permission_classes = (IsAdmin,)
    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        data = {}
        password = generate_password()
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user
        serializer.validated_data['password'] = password
        account = serializer.save()
        data['response'] = 'successfully registered a new user.'
        data['id'] = account.id
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        data['phone'] = account.phone
        data['email'] = account.email
        data['password'] = password
        data['location'] = account.location

        return Response(data)

class AdminRegisterView(APIView):
    permission_classes = (IsSuperUser,)
    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)

        data = {}
        serializer.is_valid(raise_exception=True)
        account = serializer.save(user=request.user)
        data['response'] = 'successfully registered a new user.'
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        data['id'] = account.id

        return Response(data)

class GetAdminStaffView(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request):
        try:
            objs = User.objects.filter(user=request.user.id, is_deleted=False).order_by('-id')
        except User.DoesNotExist:
            return Response({"error": "users not found"}, status=404)
        serializer = UserDetailSerializer(objs, many=True)
        data = {
            "staffs": serializer.data
        }
        return Response(data, status=200)

class UserActions(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserDetailSerializer

    def delete(self, request, pk):
        try:
            user_obj = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=404)
        if not user_obj.is_deleted:
            user_obj.is_deleted = True
            user_obj.is_active = False
            user_obj.save()
            return Response({"message": "success"}, status=200)
        else:
            return Response({"error": "user already deleted"})
        
    
class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id, is_deleted=False)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=404)
        serializer = UserDetailSerializer(user)
        data = {
            "user": serializer.data
        }
        return Response(data, status=200)

class SuperAdminRegisterView(APIView):
    permission_classes = (IsSuperUser,)
    def post(self, request):
        serializer = SuperAdminSerializer(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        account = serializer.save(user=request.user)
        data['response'] = 'successfully registered a new super admin.'
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        data['id'] = account.id
        
        return Response(data)

class GetSuperUserAdmins(APIView):
    permission_classes = (IsSuperUser,)
    def get(self, request):
        try:
            objs = User.objects.filter(user=request.user).order_by('-id')
        except User.DoesNotExist:
            return Response({"error": "admins not found"}, status=404)
        serializer = UserDetailSerializer(objs, many=True)
        data = {
            "admins": serializer.data
        }
        return Response(data, status=200)


class AllUsersView(ListAPIView):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserDetailSerializer


class ChangePasswordView(generics.GenericAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self):
            obj = self.request.user
            return obj

        def post(self, request):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                data = {
                    'status': 'success',
                    'message': 'Password updated successfully',
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"Status": "Successfully logged out!"}, status=status.HTTP_204_NO_CONTENT)



class UserLoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            if "phone" in data:
                user = authenticate(request, phone = data['phone'], password = data['password'], is_deleted=False)
            elif "email" in data:
                user = authenticate(request, email = data['email'], password = data['password'], is_deleted=False)
                
            else:
                raise ValidationError("Invalid data. Login with email or phone number")
                

            if user:
                if user.is_active==True:
                    try:
                        refresh = RefreshToken.for_user(user)
                        user_detail = {}
                        user_detail['id']   = user.id
                        user_detail['first_name'] = user.first_name
                        user_detail['last_name'] = user.last_name
                        user_detail['email'] = user.email
                        user_detail['phone'] = user.phone
                        user_detail['role'] = user.role
                        user_detail['is_admin'] = user.is_admin
                        user_detail['access'] = str(refresh.access_token)
                        user_detail['refresh'] = str(refresh)
                       

                        if user.role == 'admin':
                            user_detail["modules"] = user.module_access
                            
                        data = {
    
                        "message":"success",
                        'data' : user_detail,
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    

                    except Exception as e:
                        raise e
                
                else:
                    data = {
                    
                    'error': 'This account has not been activated'
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)

            else:
                data = {
                    'error': 'Please provide a valid email and a password'
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
                data = {
                    
                    'error': serializer.errors
                    }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)