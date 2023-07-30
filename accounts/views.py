from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status, generics
from django.contrib.auth import get_user_model
from .models import UserActivity, Organisations
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import LoginSerializer, ChangePasswordSerializer, PasswordResetSerializer, ActivitySerializer, EmailSerializer, OrganisationSerializer, UserDeleteSerializer, UserRegisterationSerializer, UserDetailSerializer, UserLogoutSerializer, SuperAdminSerializer, CreateOrganisationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from .helpers.generator import generate_password, generate_admin_password
from .helpers.sms import sign_up_sms, password_reset_sms
from .helpers.mail import signup_mail, reset_password
from .permissions import IsAdmin, IsSuperUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


class UserRegisterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdmin,)

    @swagger_auto_schema(method="post", request_body=UserRegisterationSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        password = generate_password()
        data = {}
        serializer.is_valid(raise_exception=True)
        if User.objects.filter(phone=serializer.validated_data['phone'], role="staff").exists():
            raise ValidationError({"phone": "phone number already exists for a staff"})
        serializer.validated_data['user'] = request.user
        serializer.validated_data['password'] = password
        serializer.validated_data['role'] = "staff"

        if request.user.role == 'admin':
            serializer.validated_data['organisation'] = request.user.organisation

        account = serializer.save()

        sign_up_sms(number=account.phone, pin=password)
    
        message = f"new user created by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
        data = serializer.data.copy()
        data['password'] = password

        return Response(data, status=200)


class AdminRegisterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdmin,)

    @swagger_auto_schema(method="post", request_body=CreateOrganisationSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = CreateOrganisationSerializer(data=request.data)

        data = {}

        serializer.is_valid(raise_exception=True)
        admin = serializer.validated_data.pop('admin')
        organisation = serializer.validated_data.pop('organisation')
        if User.objects.filter(phone=admin['phone'], role="admin").exists():
            raise ValidationError({"phone": "phone number already exists for an admin"})
        user = User.objects.create(is_admin=True, is_staff=True, role="admin", **admin)
        password = generate_admin_password()
        user.set_password(password)
        user.save()

        org_obj = Organisations.objects.create(**organisation)
        org_obj.contact_admin = user
        org_obj.save()
        user.organisation = org_obj
        user.save()
        
        signup_mail(email= user.email, password=password, first_name=user.first_name) 
        message = f"new user created by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
        data['response'] = 'successfully registered a new user.'
        data['id'] = user.id
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
       

        return Response(data)
 

class UserActions(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdmin,)
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserDetailSerializer


class DeleteUserView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdmin,)
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserDeleteSerializer
    
    @swagger_auto_schema(method="delete", request_body=UserDeleteSerializer())
    @action(methods=["delete"], detail=True)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if check_password(serializer.validated_data.get("current_password"), request.user.password):
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        raise PermissionDenied(detail={"error":"password incorrect"})
            


        
    
class UserProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = get_object_or_404(User, id=request.user.id)
        except Http404:
            return Response({"error": "user not found"}, status=404)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=200)
   
    
    

class SuperAdminRegisterView(APIView):
    permission_classes = (IsSuperUser,)
    authentication_classes = [JWTAuthentication]
    
    @swagger_auto_schema(method="post", request_body=SuperAdminSerializer())
    @action(methods=["post"], detail=True)
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
    authentication_classes = [JWTAuthentication]
    
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


class ChangePasswordView(generics.GenericAPIView):
        """
        An endpoint for changing password.
        """
        
        serializer_class = ChangePasswordSerializer
        model = User
        authentication_classes = [JWTAuthentication]
        permission_classes = (IsAuthenticated,)

        def get_object(self):
            obj = self.request.user
            return obj
        
        
        @swagger_auto_schema(method="post", request_body=ChangePasswordSerializer())
        @action(methods=["post"], detail=True)
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
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(method="post", request_body=UserLogoutSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"Status": "Successfully logged out!"}, status=status.HTTP_204_NO_CONTENT)



class UserLoginView(APIView):

    @swagger_auto_schema(method="post", request_body=LoginSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            if "email" in data:
                user = authenticate(request, email = data['email'], password = data['password'], is_deleted=False)
            elif "phone" in data:
                user = authenticate(request, phone = data['phone'], password = data['password'], role="staff", is_deleted=False)
                
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

            elif "email" in data:
                data = {
                    'error': 'Please provide a valid email address or password'
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            elif "phone" in data:
                data = {
                    'error': 'Please provide a valid phone number or password'
                }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {
                    'error': serializer.errors
                    }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AdminResetPassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdmin,)

    
    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"erorr": "user not found"}, status=404)
        password = generate_password()
        user.set_password(password)
        user.save()

        password_reset_sms(number=user.phone, pin=password)
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline="You reset a user password")

        data = {
            "message": "reset successful. please copy this somewhere as you would not have access to it again.",
            "password": password
        }

        return Response(data, status=200)


class AllUserActivities(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdmin,)
    serializer_class = ActivitySerializer
    queryset = UserActivity.objects.all().order_by('-id')


class OrganizationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsSuperUser,)

    def get(self, request):
        orgs = Organisations.objects.filter(is_deleted=False).order_by('-timestamp')
        serializer = OrganisationSerializer(orgs, many=True)
        return Response(serializer.data, 200)



class AllUsersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdmin,)

    def get(self, request):

        
        if request.user.role == 'admin':
            objs = User.objects.filter(organisation=request.user.organisation, is_admin=False, is_superuser=False, is_deleted=False).order_by('-timestamp')
                
        else:
            objs = User.objects.filter(is_deleted=False, is_admin=False, is_superuser=False).order_by('-timestamp')
        serializer = UserDetailSerializer(objs, many=True)
                
        return Response(serializer.data, status=200)
        


class PasswordResetView(APIView):
    serializer_class = EmailSerializer


    @swagger_auto_schema(method="post", request_body=EmailSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email, is_deleted=False).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            referer = request.META.get('HTTP_REFERER')
            reset_url = f"{referer}reset-password/{uidb64}/{token}"
            reset_password(email=email, url=reset_url)
            return Response({"message": "an email that contains new password has been sent to you"}, status=200)
        
        else:
            return Response({"error": "user not found"}, status=404)
        


class PasswordResetConfirmView(APIView):

    @swagger_auto_schema(method="post", request_body=PasswordResetSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.data.get("password"))
            user.save()
            return Response({"message": "password reset successful"}, status=200)
        
        else:
            return Response({"error": "invalid token"}, status=400)
        
class OrganisationAction(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsSuperUser,)
    queryset = Organisations.objects.filter(is_deleted=False)
    serializer_class = OrganisationSerializer




@swagger_auto_schema(method="put", request_body=CreateOrganisationSerializer())
@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def edit_organization(request, org_id, admin_id):
    
    try:
        organisation = Organisations.objects.get(id=org_id, is_deleted=False)
        user = User.objects.get(id=admin_id, is_deleted=False)
    except Organisations.DoesNotExist:
        raise NotFound(detail={"error":f"organization with id {org_id} not found"})
    except User.DoesNotExist:
        raise NotFound(detail={"error":f"user with id {admin_id} not found"})
    
    
    
    serializer = CreateOrganisationSerializer(organisation, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if (request.user != organisation.contact_admin and organisation.contact_admin != user) or (request.user.role != "superuser"):
        raise PermissionDenied({"error":"you do not have permission to perform this action"})
    
    
    serializer.update(serializer.validated_data,organisation,user)
    
    return Response({"message":"success"}, status=status.HTTP_202_ACCEPTED)
        
        



