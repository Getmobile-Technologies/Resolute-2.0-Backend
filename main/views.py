from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PanicSerializer, CallSerializer, TrackMeSerializer
from .models import PanicRequest, CallRequest, TrackMeRequest
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from accounts.serializers import UserDetailSerializer
from django.http import Http404
User = get_user_model()
from accounts.permissions import IsAdmin, IsSuperUser
from rest_framework.permissions import IsAuthenticated
from .helpers.location import user_location





class PanicView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = PanicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = user_location()

        serializer.save(user=request.user,
                        longitude=location['lon'],
                        latitude=location['lat'],
                        location=location['regionName']
                        )
        data = {
            "message": "panic request sent",
            "user": {
                "phone": request.user.phone,
                "status": location['status']
            }
        }
        return Response(data, status=200)
    

class GetPanicRequestAdmin(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        users = User.objects.filter(user=request.user.id)
        
        data = []
        for user in users:
            panic_requests = PanicRequest.objects.filter(user=user).order_by('-id')
            for panic_request in panic_requests:
                serializer = PanicSerializer(panic_request)
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


class AllPanicRequest(generics.ListAPIView):
    queryset = PanicRequest.objects.all().order_by('-id')
    permission_classes = (IsAdmin,)
    serializer_class = PanicSerializer

    
class CallRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = CallSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, phone=request.user.phone)
        data = {
            "message": "call request successful",
            "id": request.user.id
        }
        return Response(data, status=200)


class GetCallRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        users = User.objects.filter(user=request.user.id)
        
        data = []
        for user in users:
            call_requests = CallRequest.objects.filter(user=user).order_by('-id')
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


class TotalIncidentView(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request):
        try:
            users = User.objects.filter(user_id=request.user.id)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=404)
        # for user in users:
        panic = PanicRequest.objects.filter(user_id__in= users, is_reviewed=True).count()

        return Response({"total incident": panic}, status=200)

class ReviewedIncident(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request):
        try:
            users = User.objects.filter(user_id=request.user.id)
            for user in users:
                panics = PanicRequest.objects.filter(user_id=user.id, is_reviewed=True)
                amt = panics.count()
                

            return Response({"reviewed incident": amt}, status=200)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=404)
       


class TrackMeRequestView(APIView):
    def post(self, request):
        serializer = TrackMeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = user_location()

        serializer.save(user=request.user,
                        longitude=location['lon'],
                        latitude=location['lat'],
                        location=location['regionName']
                        )
        data = {
            "message": "tracking request sent",
            "user": {
                "phone": request.user.phone,
                "status": location['status']
            }
        }
        return Response(data, status=200)

class GetTrackMeRequestAdmin(APIView):
    permission_classes = (IsAdmin,)
 
    def get(self, request):
        users = User.objects.filter(user=request.user)
        
        data = []
        for user in users:
            track_requests = TrackMeRequest.objects.filter(user=user).order_by('-id')
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
