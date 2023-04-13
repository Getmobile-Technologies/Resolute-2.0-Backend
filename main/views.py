from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PanicSerializer, CallSerializer
from .models import PanicRequest, CallRequest
from django.contrib.auth import get_user_model
from django.http import Http404
User = get_user_model()
from accounts.permissions import IsAdmin, IsSuperUser
from rest_framework.permissions import IsAuthenticated





class PanicView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = PanicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        data = {
            "message": "panic request sent",
            "user": {
                "id": request.user.id
            }
        }
        return Response(data, status=200)
    
class GetPanicRequestAdmin(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request):
        try:
            users = User.objects.filter(user=request.user.id)
        except Http404:
            return Response({"error": "user not found"}, status=404)
        for user in users:
            objs = PanicRequest.objects.filter(user=user.user)
            serializer = PanicSerializer(objs, many=True)
            data = {
                "request": serializer.data
            }

        return Response(data, status=200)

class PanicReview(APIView):
    permission_classes = (IsSuperUser,)
    def post(self, request, pk):
        try:
            obj = PanicRequest.objects.get(id=pk)
        except PanicRequest.DoesNotExist:
            return Response({"error": "reqeust not found"}, status=404)
        if not obj.IsReviewed:
            obj.IsReviewed = True
            obj.save()
            return Response({"message": "review success"}, status=200)
        else:
            return Response({"error": "request already reviewed"}, status=400)


class SuperAdminPanicView(APIView):
    permission_classes = (IsSuperUser,)

    def get(self, request):
        try:
            objs = PanicRequest.objects.all().order_by()
        except PanicRequest.DoesNotExist:
            return Response({"error": "request not found"}, status=404)
        serializer = PanicSerializer(objs, many=True)
        data = {
            "all request": serializer.data
        }

        return Response(data, status=200)
    
class CallRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = CallSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        data = {
            "message": "call request successful",
            "id": request.user.id
        }
        return Response(data, status=200)
    

class GetCallRequestAdmin(APIView):
    def get(self, request):
        try:
            users = User.objects.filter(user=request.user.id)
        except Http404:
            return Response({"error": "user not found"}, status=404)
        for user in users:
            objs = CallRequest.objects.filter(user=user.user)
            serializer = CallSerializer(objs, many=True)
            data = {
                "request": serializer.data
            }

        return Response(data, status=200)



[1, 2, 3, 4, 5, 6, 7 ]



{
    2:{
    2, 3, 4, 
    }
}