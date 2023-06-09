from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PanicSerializer, CallSerializer, TrackMeSerializer, FirebaseSerializer, LocationSerializer, EmergencySerializer, ImageSerializer, NotificationSerializer, CatgorySerializer
from .models import PanicRequest, CallRequest, TrackMeRequest, StaffLocation, Images, Notifications, Category, EmergencyContact
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from accounts.serializers import UserDetailSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from accounts.permissions import IsAdmin, IsSuperUser
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserActivity
from .signals import send_emergency_sms
from accounts.helpers.sms import emergency_sms, geocoding
from .helpers.notify import notification_handler
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()





class PanicView(APIView):
    permission_classes = (IsAuthenticated,)
    
    
    @swagger_auto_schema(method="post", request_body=PanicSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = PanicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['organisation'] = request.user.organisation
        serializer.validated_data['user_location'] = request.user.location.state
        serializer.save(user=request.user)

        notification_handler(organisation=request.user.organisation,
                             message=f"New panic alert from {request.user.first_name}")
        
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline="You made a new panic alert")
        
        data = {
            "message": "panic request sent",
            "user": {
                "phone": request.user.phone
            }
        }
        return Response(data, status=200)
    

class GetPanicRequests(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        if request.user.role == 'admin':
            panic = PanicRequest.objects.filter(organisation=request.user.organisation, is_deleted=False).order_by('-timestamp')
        else:
            panic = PanicRequest.objects.filter(is_deleted=False).order_by('-timestamp')

        serializer = PanicSerializer(panic, many=True)

        return Response(serializer.data, status=200)
            

class PanicActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = PanicRequest.objects.filter(is_deleted=False).order_by('-timestamp')
    serializer_class = PanicSerializer



class PanicReview(APIView):
    permission_classes = (IsAdmin,)
    
    @swagger_auto_schema(method="post", request_body=PanicSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.is_reviewed:
            obj.is_reviewed = True
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)
        
    
    def delete(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if obj.is_reviewed:
            obj.is_reviewed = False
            obj.save()
            return Response({"message": "unreviewed!"}, status=200)
        else:
            return Response({"error": "request not reviewed"}, status=400)

class PanicGenuineView(APIView):
    permission_classes = (IsAdmin,)
    
    
    def post(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if obj.is_genuine:
            obj.is_genuine = False
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)
        
    def delete(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.is_genuine:
            obj.is_genuine = True
            obj.save()
            return Response({"message": "unreviewed!"}, status=200)
        else:
            return Response({"error": "request not reviewed"}, status=400)


class AllPanicRequest(generics.ListAPIView):
    queryset = PanicRequest.objects.filter(is_deleted=False).order_by('-timestamp')
    permission_classes = (IsAdmin,)
    serializer_class = PanicSerializer

    
class CallRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(method="post", request_body=CallSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = CallSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['organisation'] = request.user.organisation
        serializer.save(user=request.user, phone=request.user.phone)

        notification_handler(organisation=request.user.organisation,
                             message=f"New call alert from {request.user.first_name}")
        
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline="You made a call panic alert")

        data = {
            "message": "call request successful",
            "id": request.user.id
        }
        return Response(data, status=200)

class CallRequestActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = CallRequest.objects.filter(is_deleted=False)
    serializer_class = CallSerializer


class GetCallRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        if request.user.role == 'admin':
            call = CallRequest.objects.filter(organisation=request.user.organisation, is_deleted=False)
        else:
            call = CallRequest.objects.filter(is_deleted=False)

        serializer = CallSerializer(call, many=True)

        return Response(serializer.data, status=200)
           
        

class CallReview(APIView):
    permission_classes = (IsAdmin,)
    
    def post(self, request, pk):
        try:
            obj = CallRequest.objects.get(id=pk)
        except CallRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.is_reviewed:
            obj.is_reviewed = True
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)

    def delete(self, request, pk):
        try:
            obj = CallRequest.objects.get(id=pk)
        except CallRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if obj.is_reviewed:
            obj.is_reviewed = False
            obj.save()
            return Response({"message": "unreviewed!"}, status=200)
        else:
            return Response({"error": "request not reviewed"}, status=400)


class IncidentCounts(APIView):
    permission_classes = (IsAdmin,)
    
    def get(self, request):
        if request.user.role == 'admin':
            try:
                user_obj = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                return Response({"error": "user not found"}, status=404)
            total_panic = user_obj.total_admin_panic
            total_reviewed = user_obj.total_reviewed_panic
            total_unreviewed = user_obj.total_unreviewed_panic
            total_ingenuine = user_obj.total_ingenuine_panic

            data = {
                "total_incident": total_panic,
                "reviewed_incident": total_reviewed,
                "un_reviewed_incident": total_unreviewed,
               "ingenuine_incident": total_ingenuine
            }

            return Response(data, status=200)
        
        else:
            total_incident = PanicRequest.objects.filter(is_deleted=False).count()
            reviewed_incident = PanicRequest.objects.filter(is_reviewed=True).count()
            un_reviewed_incident = PanicRequest.objects.filter(is_reviewed=False).count()
            ingenuine_incident = PanicRequest.objects.filter(is_genuine=False).count()

            data = {
                "total_incident": total_incident,
                "reviewed_incident": reviewed_incident,
                "un_reviewed_incident": un_reviewed_incident,
                "ingenuine_incident": ingenuine_incident
            }

            return Response(data, status=200)
       


class TrackMeRequestView(APIView):
    
    @swagger_auto_schema(method="post", request_body=TrackMeSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = TrackMeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['organisation'] = request.user.organisation
        serializer.save(user=request.user)
        notification_handler(organisation=request.user.organisation,
                             message=f"New Track alert from {request.user.first_name}")
        
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline="You made a track alert")

        data = {
            "message": "tracking request sent",
            "user": {
                "phone": request.user.phone,
            }
        }
        return Response(data, status=200)
    

class TrackActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = TrackMeRequest.objects.filter(is_deleted=False)
    serializer_class = TrackMeSerializer

        
        
class GetTrackMeRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        if request.user.role == 'admin':

            track = TrackMeRequest.objects.filter(organisation=request.user.organisation, is_deleted=False).order_by('-timestamp')
        else:
            track = TrackMeRequest.objects.filter(is_deleted=False).order_by('-timestamp')

        serializer = TrackMeSerializer(track, many=True)

        return Response(serializer.data, status=200)
            
        
class TrackMeReview(APIView):
    permission_classes = (IsAdmin,)
    def post(self, request, pk):
        try:
            obj = TrackMeRequest.objects.get(id=pk)
        except TrackMeRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.is_reviewed:
            obj.is_reviewed = True
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)
    def delete(self, request, pk):
        try:
            obj = TrackMeRequest.objects.get(id=pk)
        except TrackMeRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if obj.is_reviewed:
            obj.is_reviewed = False
            obj.save()
            return Response({"message": "unreviewed!"}, status=200)
        else:
            return Response({"error": "request not reviewed"}, status=400)


class LocationCreateView(APIView):
    permission_classes = (IsAdmin,)
    
    @swagger_auto_schema(method="post", request_body=LocationSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data['city']
        state = serializer.validated_data['state']
        if StaffLocation.objects.filter(city=city, state=state, organisation=request.user.organisation, is_deleted=False).exists():
            return Response({"error": "location already exist"}, status=400)
        
        if request.user.role == "admin":
            serializer.validated_data['organisation'] = request.user.organisation
        
        serializer.validated_data['admin'] = request.user
        serializer.save(user=request.user)
        message = f"new location created by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
        return Response({"message": "location created"}, status=200)
    


class GetLocations(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request):
        if request.user.role == "admin":
            locations = StaffLocation.objects.filter(organisation=request.user.organisation, is_deleted=False).order_by('-timestamp')

        else:
            locations = StaffLocation.objects.filter(is_deleted=False).order_by('-timestamp')

        serializer = LocationSerializer(locations, many=True)
        
        data = {
            "locations": serializer.data
        }
        return Response(data, status=200)



class LocationActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = StaffLocation.objects.filter(is_deleted=False)
    serializer_class = LocationSerializer


class ImageView(APIView):
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(method="post", request_body=ImageSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['organisation'] = request.user.organisation
        serializer.validated_data['user'] = request.user
        serializer.save()
        notification_handler(organisation=request.user.organisation,
                             message=f"New image alert from {request.user.first_name}")
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline="You made a image request")
        data = {
            "message": "image request successful"
            
        }
        return Response(data, status=200)


class GetImageRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        if request.user.role == 'admin':
            images = Images.objects.filter(organisation=request.user.organisation, is_deleted=False).order_by('-timestamp')
        else:
            images = Images.objects.filter(is_deleted=False).order_by('-timestamp')

        serializer = ImageSerializer(images, many=True)

        return Response(serializer.data, status=200)
            
class ImageActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = Images.objects.filter(is_deleted=False)
    serializer_class = ImageSerializer

            

class GetAdminNotifications(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        if request.user.role == "admin":
            notifications = Notifications.objects.filter(organisation=request.user.organisation, is_deleted=False).order_by('-timestamp')
        else:
            notifications = Notifications.objects.filter(is_deleted=False).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)

        return Response(serializer.data, status=200)


class NotifficationActions(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = Notifications.objects.filter(is_deleted=False)
    serializer_class = NotificationSerializer

        

class CreateCategory(APIView):
    permission_classes = (IsSuperUser,)

    @swagger_auto_schema(method="post", request_body=CatgorySerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = CatgorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        try:
            get_object_or_404(Category, name=name)
            return Response({"error": "category already exist"}, status=400)
        except Http404:
            serializer.save()
            return Response({"message": "new category created"}, status=200)
    
    def get(self, request):
        try:
            obj = Category.objects.filter(is_deleted=False)
            serializer = CatgorySerializer(obj, many=True)
            data = {
                "categories": serializer.data
            }
            return Response(data, status=200)
        except Category.DoesNotExist:
            return Response({"error": "category not found"}, status=404)


class CategoryActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = CatgorySerializer
    queryset = Category.objects.filter(is_deleted=False)



class LocationIncidentCount(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        if request.user.role == "admin":
            try:
                locations = StaffLocation.objects.filter(organisation=request.user.organisation, is_deleted=False)
            except StaffLocation.DoesNotExist:
                return Response({"error": "not found"}, status=404)
            data = []
            for location in locations:
                panic = PanicRequest.objects.filter(user_location=location.state, is_deleted=False).count()
                resolved = PanicRequest.objects.filter(user_location=location.state, is_deleted=False, is_reviewed=True).count()
                unresolved = PanicRequest.objects.filter(user_location=location.state, is_deleted=False, is_reviewed=False).count()
                request_data = {
                    "state": location.state,
                    "panic_count": panic,
                    "panic_resolved": resolved,
                    "panic_unresolved": unresolved
                }
                data.append(request_data)
            return Response(data, status=200)
        else:
            try:
                locations = StaffLocation.objects.filter(is_deleted=False)
            except StaffLocation.DoesNotExist:
                return Response({"error": "not found"}, status=404)
            data = []
            for location in locations:
                panic = PanicRequest.objects.filter(user_location=location.state, is_deleted=False).count()
                resolved = PanicRequest.objects.filter(user_location=location.state, is_deleted=False, is_reviewed=True).count()
                unresolved = PanicRequest.objects.filter(user_location=location.state, is_deleted=False, is_reviewed=False).count()
                request_data = {
                    "state": location.state,
                    "panic_count": panic,
                    "panic_resolved": resolved,
                    "panic_unresolved": unresolved
                }
                data.append(request_data)
            return Response(data, status=200)



class EmergencyContactView(APIView):
    permission_classes = (IsSuperUser,)

    @swagger_auto_schema(method="post", request_body=EmergencySerializer())
    @action(methods=["post"], detail=True)
    def post(self, request):
        serializer = EmergencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "emergency contact added succesfuly"}, status=200)
    
    def get(self, request):
        contacts = EmergencyContact.objects.filter(is_deleted=False).order_by('-timestamp')
        serializer = EmergencySerializer(contacts, many=True)

        data = {
            "contacts": serializer.data
        }

        return Response(data, status=200)
    
class EmergencyActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = EmergencySerializer
    queryset = EmergencyContact.objects.filter(is_deleted=False)

class FireBaseResetToken(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        """Update the FCM token for a logged in user to enable push notifications

        Returns:
            Json response with message of success and status code of 200.
        """
        
        serializer = FirebaseSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        fcm_token = serializer.validated_data.get("fcm_token")

        request.user.fcm_token = fcm_token
        request.user.save()
            
        return Response({"message": "success"}, status=status.HTTP_200_OK)