import email
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from .models import UserActivity, Organisations
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import LoginSerializer, ChangePasswordSerializer, ActivitySerializer, UserRegisterationSerializer, UserDetailSerializer, UserLogoutSerializer, SuperAdminSerializer, CreateOrganisationSerializer
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

        try:
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['user'] = request.user
            serializer.validated_data['password'] = password
            serializer.validated_data['open_password'] = password
            serializer.validated_data['organisation'] = request.user.organisation
            account = serializer.save()
        except IntegrityError as e:
            data['response'] = 'error registering a new user.'
            data['error'] = str(e)
            return Response(data, status=400)
        message = f"new user created by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
        data['response'] = 'successfully registered a new user.'
        data['id'] = account.id
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        data['phone'] = account.phone
        data['email'] = account.email
        data['password'] = password
        data['location'] = account.location
        data['organisation'] = account.organisation

        return Response(data)


class AdminRegisterView(APIView):
    permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = CreateOrganisationSerializer(data=request.data)

        data = {}

        try:
            serializer.is_valid(raise_exception=True)
            admin = serializer.validated_data.pop('admin')
            organisation = serializer.validated_data.pop('organisation')
            name = organisation['name']
            try:
                get_object_or_404(Organisations, name=name)
                return Response({"error": "organisation already exist"}, status=400)
            except Http404:
                org_obj = Organisations.objects.create(**organisation)
                user = User.objects.create(user=request.user, organisation=org_obj.name, category=org_obj.category, is_admin=True, is_staff=True, **admin)
                user.set_password(user.password)
                user.save()
                org_obj.contact_admin = user
                org_obj.save()
        except IntegrityError as e:
            data['response'] = 'error registering a new user.'
            data['error'] = str(e)
            return Response(data, status=400)
        
        message = f"new user created by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
        data['response'] = 'successfully registered a new user.'
        data['id'] = user.id
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
       

        return Response(data)
 

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
            objs = User.objects.filter(is_deleted=False, is_admin=True, is_superuser=False).order_by('-id')
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
                        user_logged_in.send(sender=user.__class__,
                                            request=request, user=user)
                        message = f"{user.role} member login"
                        UserActivity.objects.create(user=user, organisation=user.organisation, timeline=message)
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


class AdminResetPassword(APIView):
    permission_classes = (IsAdmin,)

    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"erorr": "user not found"}, status=404)
        password = generate_password()
        user.set_password(password)
        user.open_password = password
        user.save()
        message = f"{request.user.role} reset user password"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
        data = {
            "message": "reset successful",
            "password": password
        }

        return Response(data, status=200)


   
class GetAdminStaffView(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request):
        try:
            objs = User.objects.filter(organisation=request.user.organisation, is_admin=False, is_superuser=False, is_deleted=False).order_by('-id')
        except User.DoesNotExist:
            return Response({"error": "users not found"}, status=404)
        serializer = UserDetailSerializer(objs, many=True)
        data = {
            "staffs": serializer.data
        }
        return Response(data, status=200)
    


class AllUserActivities(generics.ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = ActivitySerializer
    queryset = UserActivity.objects.all().order_by('-id')


class OrganizationView(APIView):
    permission_classes = (IsSuperUser,)

    def get(self, request):
        orgs = Organisations.objects.filter(is_deleted=False)
        data = []
        for org in orgs:
            user = User.objects.get(id=org.contact_admin)
            sum = User.objects.filter(organisation=org.name).count()

            request_data = {
                "id": org.id,
                "organisation": org.name,
                "category": org.category,
                "total_registered_users": sum,
                "contact_admin": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "email": user.email
                }
            }
            data.append(request_data)
        return Response(data, status=200)


