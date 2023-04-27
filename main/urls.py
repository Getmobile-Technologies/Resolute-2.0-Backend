from django.urls import path
from . import views




urlpatterns = [
    path('create/panic/request', views.PanicView.as_view()),
    path('admin/panic/requests', views.GetPanicRequestAdmin.as_view()),
    path('create/call/request', views.CallRequestView.as_view()),
    path('panic/review/<int:pk>', views.PanicReview.as_view()),
    path('panic/all', views.AllPanicRequest.as_view()),
    path('incidents/count', views.IncidentCounts.as_view()),
    path('call/review/<int:pk>', views.CallReview.as_view()),
    path('create/track/requests', views.TrackMeRequestView.as_view()),
    path('admin/call/requests', views.GetCallRequestAdmin.as_view()),
    path('trackme/review/<int:pk>', views.TrackMeReview.as_view()),
    path('admin/track/requests', views.GetTrackMeRequestAdmin.as_view()),
    path('create/location', views.LocationCreateView.as_view()),
    path('all/admins/location', views.GetAdminLocations.as_view()),
    path('create/image/request', views.ImageView.as_view()),
    path('admin/image/requests', views.GetImageRequestAdmin.as_view()),
    path('location/actions/<int:pk>', views.LocationActions.as_view()),
    path('image/actions/<int:pk>', views.ImageActions.as_view())
]