from django.urls import path, include
from . import views




urlpatterns = [
    path('create/panic/request', views.PanicView.as_view()),
    path('admin/panic/requests', views.GetPanicRequestAdmin.as_view()),
    path('panic/review', views.PanicReview.as_view()),
    path('panic/reviewed/view', views.SuperAdminPanicView.as_view())

]