from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PanicSerializer, CallSerializer, TrackMeSerializer, LocationSerializer, EmergencySerializer, ImageSerializer, NotificationSerializer, CatgorySerializer
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
User = get_user_model()

def notification_handler(user, status):
    notify = Notifications.objects.create(user=user, status=status)

    return notify



class PanicView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = PanicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['organisation'] = request.user.organisation
        serializer.validated_data['state'] = request.user.state
        serializer.save(user=request.user)
        status = "new panic request"
        notification_handler(user=request.user, status=status)
        message = f"new panic request made by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
        
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
            users = User.objects.filter(organisation=request.user.organisation, is_deleted=False)
            data = []
            for user in users:
                panic_requests = PanicRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
                for panic_request in panic_requests:
                    serializer = PanicSerializer(panic_request)
                    request_data = {
                        "id": serializer.data['id'],
                        "longitude": serializer.data['longitude'],
                        "latitude": serializer.data['latitude'],
                        "location": serializer.data['location'],
                        "is_reviewed": serializer.data['is_reviewed'],
                        "is_genuine": serializer.data['is_genuine'],
                        "timestamp": serializer.data['timestamp'],
                        "user": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "location": user.location,
                            "phone": user.phone,
                            "role": user.role
                        }
                    }
                    data.append(request_data)

            return Response(data, status=200)
        else:
            users = User.objects.filter(is_deleted=False)
            data = []
            for user in users:
                panic_requests = PanicRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
                for panic_request in panic_requests:
                    serializer = PanicSerializer(panic_request)
                    request_data = {
                        "id": serializer.data['id'],
                        "longitude": serializer.data['longitude'],
                        "latitude": serializer.data['latitude'],
                        "location": serializer.data['location'],
                        "is_reviewed": serializer.data['is_reviewed'],
                        "is_genuine": serializer.data['is_genuine'],
                        "timestamp": serializer.data['timestamp'],
                        "organisation": user.organisation,
                        "user": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "location": user.location,
                            "phone": user.phone,
                            "role": user.role
                        }
                    }
                    data.append(request_data)

            return Response(data, status=200)

class PanicActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = PanicRequest.objects.filter(is_deleted=False)
    serializer_class = PanicSerializer



class PanicReview(APIView):
    permission_classes = (IsAdmin,)
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
    queryset = PanicRequest.objects.filter(is_deleted=False).order_by('-id')
    permission_classes = (IsAdmin,)
    serializer_class = PanicSerializer

    
class CallRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = CallSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['organisation'] = request.user.organisation
        serializer.save(user=request.user, phone=request.user.phone)
        status = "new call request"
        notification_handler(user=request.user, status=status)
        message = f"new call request made by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
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
            users = User.objects.filter(organisation=request.user.organisation, is_deleted=False)
            data = []
            for user in users:
                call_requests = CallRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
                for call_request in call_requests:
                    serializer = CallSerializer(call_request)
                    request_data = {
                        "id": serializer.data['id'],
                        "phone": serializer.data['phone'],
                        "is_reviewed": serializer.data['is_reviewed'],
                        "timestamp": serializer.data['timestamp'],
                        "user": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "location": user.location,
                            "phone": user.phone,
                            "role": user.role
                        }
                    }
                    data.append(request_data)

            return Response(data, status=200)
        else:
            users = User.objects.filter(is_deleted=False)
            data = []
            for user in users:
                call_requests = CallRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
                for call_request in call_requests:
                    serializer = CallSerializer(call_request)
                    request_data = {
                        "id": serializer.data['id'],
                        "phone": serializer.data['phone'],
                        "is_reviewed": serializer.data['is_reviewed'],
                        "timestamp": serializer.data['timestamp'],
                        "organisation": user.organisation,
                        "user": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "location": user.location,
                            "phone": user.phone,
                            "role": user.role
                        }
                    }
                    data.append(request_data)

            return Response(data, status=200)
        

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
    def post(self, request):
        serializer = TrackMeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['organisation'] = request.user.organisation
        serializer.save(user=request.user)
        status = "new track me request"
        notification_handler(user=request.user, status=status)
        message = f"new track request made by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
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
            users = User.objects.filter(organisation=request.user.organisation, is_deleted=False)
            data = []
            for user in users:
                track_requests = TrackMeRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
                for track_request in track_requests:
                    serializer = TrackMeSerializer(track_request)
                    request_data = {
                        "id": serializer.data['id'],
                        "longitude": serializer.data['longitude'],
                        "latitude": serializer.data['latitude'],
                        "location": serializer.data['location'],
                        "is_reviewed": serializer.data['is_reviewed'],
                        "timestamp": serializer.data['timestamp'],
                        "user": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "location": user.location,
                            "phone": user.phone,
                            "role": user.role
                        }
                    }
                    data.append(request_data)

            return Response(data, status=200)
        else:
            users = User.objects.filter(is_deleted=False)
            data = []
            for user in users:
                track_requests = TrackMeRequest.objects.filter(user=user, is_deleted=False).order_by('-id')
                for track_request in track_requests:
                    serializer = TrackMeSerializer(track_request)
                    request_data = {
                        "id": serializer.data['id'],
                        "longitude": serializer.data['longitude'],
                        "latitude": serializer.data['latitude'],
                        "location": serializer.data['location'],
                        "is_reviewed": serializer.data['is_reviewed'],
                        "timestamp": serializer.data['timestamp'],
                        "organisation": user.organisation,
                        "user": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "location": user.location,
                            "phone": user.phone,
                            "role": user.role
                        }
                    }
                    data.append(request_data)

            return Response(data, status=200)


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
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data['city']
        state = serializer.validated_data['state']
        try:
            get_object_or_404(StaffLocation, city=city, state=state)
            return Response({"error": "location already exist"}, status=400)
        except Http404:
            serializer.validated_data['organisation'] = request.user.organisation
            serializer.save(user=request.user)
            message = f"new location created by {request.user.role}"
            UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
            return Response({"message": "location created"}, status=200)
    
class GetLocations(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request):
        if request.user.role == "admin":
            try:
                locations = StaffLocation.objects.filter(organisation=request.user.organisation, is_deleted=False)
            except StaffLocation.DoesNotExist:
                return Response({"error": "location not found"}, status=404)
            serializer = LocationSerializer(locations, many=True)
            data = {
                "locations": serializer.data
            }

            return Response(data, status=200)
        else:
            try:
                locations = StaffLocation.objects.filter(is_deleted=False)
            except StaffLocation.DoesNotExist:
                return Response({"error": "locations not found"}, status=404)
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
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['organisation'] = request.user.organisation
        serializer.validated_data['user'] = request.user
        serializer.save()
        status = "new image request"
        notification_handler(user=request.user, organisation=request.user.organisation, status=status)
        message = f"new image request made by {request.user.role}"
        UserActivity.objects.create(user=request.user, organisation=request.user.organisation, timeline=message)
        data = {
            "message": "image request successful"
            
        }
        return Response(data, status=200)


class GetImageRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        if request.user.role == 'admin':
                
            users = User.objects.filter(organisation=request.user.organisation, is_deleted=False)
            data = []
            for user in users:
                image_requests = Images.objects.filter(user=user, is_deleted=False).order_by('-id')
                for image_request in image_requests:
                    serializer = ImageSerializer(image_request)
                    request_data = {
                        "id": serializer.data['id'],
                        "image": serializer.data['image'],
                        "image2": serializer.data['image2'],
                        "image3": serializer.data['image3'],
                        "image4": serializer.data['image4'],
                        "description": serializer.data['description'],
                        "location": serializer.data['location'],
                        "is_reviewed": serializer.data['is_reviewed'],
                        "timestamp": serializer.data['timestamp'],
                        "user": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "location": user.location,
                            "phone": user.phone,
                            "role": user.role
                        }
                    }
                    data.append(request_data)

            return Response(data, status=200)
        
        else:
            users = User.objects.filter(is_deleted=False)
            data = []
            for user in users:
                image_requests = Images.objects.filter(user=user, is_deleted=False).order_by('-id')
                for image_request in image_requests:
                    serializer = ImageSerializer(image_request)
                    request_data = {
                        "id": serializer.data['id'],
                        "image": serializer.data['image'],
                        "image2": serializer.data['image2'],
                        "image3": serializer.data['image3'],
                        "image4": serializer.data['image4'],
                        "description": serializer.data['description'],
                        "location": serializer.data['location'],
                        "is_reviewed": serializer.data['is_reviewed'],
                        "timestamp": serializer.data['timestamp'],
                        "organisation": user.organisation,
                        "user": {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "location": user.location,
                            "phone": user.phone,
                            "role": user.role
                        }
                    }
                    data.append(request_data)

            return Response(data, status=200)
        

class ImageActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = Images.objects.filter(is_deleted=False)
    serializer_class = ImageSerializer

            

class GetAdminNotifications(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        users = User.objects.filter(user=request.user)
        data = []
        for user in users:
            notifications = Notifications.objects.filter(user=user, is_deleted=False).order_by('-id')
            for notification in notifications:
                serializer = NotificationSerializer(notification)

                data.append(serializer.data)
        return Response(data, status=200)


class NotifficationActions(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAdmin,)
    queryset = Notifications.objects.filter(is_deleted=False)
    serializer_class = NotificationSerializer

        

class CreateCategory(APIView):
    permission_classes = (IsSuperUser,)

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
                locate = location.state
                panic = PanicRequest.objects.filter(state=locate.lower(), is_deleted=False).count()
                request_data = {
                    "state": location.state,
                    "panic_count": panic
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
                locate = location.state
                panic = PanicRequest.objects.filter(state=locate.lower(), is_deleted=False).count()
                request_data = {
                    "state": location.state,
                    "panic_count": panic
                }
                data.append(request_data)
            return Response(data, status=200)



class EmergencyContactView(APIView):
    permission_classes = (IsSuperUser,)

    def post(self, request):
        serializer = EmergencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "emergency contact added succesfuly"}, status=200)
    
    def get(self, request):
        try:
            contacts = EmergencyContact.objects.filter(is_deleted=False).order_by('-id')
        except EmergencyContact.DoesNotExist:
            return Response({"error": "error fetching data"}, status=404)
        serializer = EmergencySerializer(contacts, many=True)

        data = {
            "contacts": serializer.data
        }

        return Response(data, status=200)
    
class EmergencyActions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = EmergencySerializer
    queryset = EmergencyContact.objects.filter(is_deleted=False)
