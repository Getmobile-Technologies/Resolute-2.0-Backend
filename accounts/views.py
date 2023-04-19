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
from .serializers import LoginSerializer, ChangePasswordSerializer, UserRegisterationSerializer, UserDetailSerializer, UserLogoutSerializer, AdminRegistrationSerializer, SuperAdminSerializer, AdminLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404
from django.http import Http404
from .permissions import IsAdmin, IsSuperUser
User = get_user_model()


class UserRegisterView(APIView):
    permission_classes = (IsAdmin,)
    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        account = serializer.save(user=request.user)
        data['response'] = 'successfully registered a new user.'
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        data['id'] = account.id

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
            objs = User.objects.filter(user=request.user.id)
        except User.DoesNotExist:
            return Response({"error": "users not found"}, status=404)
        serializer = UserDetailSerializer(objs, many=True)
        data = {
            "staffs": serializer.data
        }
        return Response(data, status=200)

class UserActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    
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

class GetSuperUserAdmins(APIView):
    permission_classes = (IsSuperUser,)
    def get(self, request):
        try:
            objs = User.objects.filter(user=request.user)
        except User.DoesNotExist:
            return Response({"error": "admins not found"}, status=404)
        serializer = UserDetailSerializer(objs, many=True)
        data = {
            "admins": serializer.data
        }
        return Response(data, status=200)


class AllUsersView(ListAPIView):
    queryset = User.objects.all()
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
        serializer.is_valid(raise_exception=True)
        try:
            user = get_object_or_404(User, phone=serializer.validated_data['phone'])
            password = user.check_password(serializer.validated_data['password'])
            if user and password:
                if user.is_staff:
                    try:
                        refresh = RefreshToken.for_user(user)
                        user_details = {}
                        user_details['id'] = user.id
                        user_details['role'] = user.role
                        user_details['access_token'] = str(refresh.access_token)
                        user_details['refresh_token'] = str(refresh)
                        user_logged_in.send(sender=user.__class__,
                                            request=request, user=user)

                        data = {
                            'message' : "User Login successful",
                            'data' : user_details,
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    except Exception as e:
                        raise e
                else:
                    return Response({"error": "unathourized login"}, status=403)
            else:
                data = {
                    'message'  : "failed",
                    'errors': 'check password and try again'
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        except Http404:
            return Response({"error": "invalid login data"}, status=400)


class AdminLoginView(APIView):

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = get_object_or_404(User, email=serializer.validated_data['email'])
            password = user.check_password(serializer.validated_data['password'])
            if user and password:
                if user.is_staff:
                    try:
                        refresh = RefreshToken.for_user(user)
                        user_details = {}
                        user_details['id'] = user.id
                        user_details['email'] = user.email
                        user_details['role'] = user.role
                        user_details['access_token'] = str(refresh.access_token)
                        user_details['refresh_token'] = str(refresh)
                        user_logged_in.send(sender=user.__class__,
                                            request=request, user=user)

                        data = {
                            'message' : "Admin Login successful",
                            'data' : user_details,
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    except Exception as e:
                        raise e

                else:
                    return Response({"error": "unathorized login"}, status=403)
            else:
                data = {
                    'message'  : "failed",
                    'errors': 'The account is not active'
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        except Http404:
                return Response({"error": "invalid data"}, status=400)
