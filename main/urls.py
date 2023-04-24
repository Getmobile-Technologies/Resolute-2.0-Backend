from django.urls import path
from . import views




urlpatterns = [
    path('create/panic/request', views.PanicView.as_view()),
    path('admin/panic/requests', views.GetPanicRequestAdmin.as_view()),
    path('create/call/request', views.CallRequestView.as_view()),
    path('panic/review/<int:pk>', views.PanicReview.as_view()),
    path('panic/all', views.AllPanicRequest.as_view()),
    path('incidents/total', views.TotalIncidentView.as_view()),
    path('incidents/reviewed/total', views.ReviewedIncident.as_view()),
    path('call/review/<int:pk>', views.CallReview.as_view()),
    path('create/track/requests', views.TrackMeRequestView.as_view()),
    path('admin/call/requests', views.GetCallRequestAdmin.as_view()),
    path('trackme/review/<int:pk>', views.TrackMeReview.as_view()),
    path('admin/track/requests', views.GetTrackMeRequestAdmin.as_view())
]