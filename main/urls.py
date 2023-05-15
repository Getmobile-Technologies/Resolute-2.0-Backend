from django.urls import path
from . import views




urlpatterns = [
    path('create/panic/request', views.PanicView.as_view()),
    path('admin/panic/requests', views.GetPanicRequests.as_view()),
    path('create/call/request', views.CallRequestView.as_view()),
    path('panic/review/<int:pk>', views.PanicReview.as_view()),
    path('panic/all', views.AllPanicRequest.as_view()),
    path('incidents/count', views.IncidentCounts.as_view()),
    path('call/review/<int:pk>', views.CallReview.as_view()),
    path('create/track/requests', views.TrackMeRequestView.as_view()),
    path('admin/call/requests', views.GetCallRequestAdmin.as_view()),
    path('trackme/review/<int:pk>', views.TrackMeReview.as_view()),
    path('admin/track/requests', views.GetTrackMeRequestAdmin.as_view()),
    path('create/locations', views.LocationCreateView.as_view()),
    path('all/location', views.GetLocations.as_view()),
    path('create/image/request', views.ImageView.as_view()),
    path('admin/image/requests', views.GetImageRequestAdmin.as_view()),
    path('location/actions/<int:pk>', views.LocationActions.as_view()),
    path('image/actions/<int:pk>', views.ImageActions.as_view()),
    path('panic/actions/<int:pk>', views.PanicActions.as_view()),
    path('call/actions/<int:pk>', views.CallRequestActions.as_view()),
    path('track/actions/<int:pk>', views.TrackActions.as_view()),
    path('get/admin/notifications', views.GetAdminNotifications.as_view()),
    path('notification/actions/<int:pk>', views.NotifficationActions.as_view()),
    path('panic/genuine/review/<int:pk>', views.PanicGenuineView.as_view()),
]