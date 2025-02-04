from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView   
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path



urlpatterns = [
    path('register/user', views.UserRegisterView.as_view()),
    path('register/admin', views.AdminRegisterView.as_view()),
    path('register/superuser', views.SuperAdminRegisterView.as_view()),
    path('single/user/<int:pk>', views.UserActions.as_view()),
    path('single/user/<int:pk>/delete', views.DeleteUserView.as_view()),
    path('user/profile', views.UserProfile.as_view()),
    path('user/login', views.UserLoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('password', views.ChangePasswordView.as_view()),
    path('refresh', TokenRefreshView().as_view(), name="refresh_token"),
    path('auth/', include('djoser.urls')),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('djoser/', include('djoser.urls')),
    path('all/users', views.AllUsersView.as_view()),
    path('superadmin/admins', views.GetSuperUserAdmins.as_view()),
    path('reset/user/password/<int:pk>', views.AdminResetPassword.as_view()),
    path('user/activities', views.AllUserActivities.as_view()),
    path('organizations', views.OrganizationView.as_view()),
    path('reset/password', views.PasswordResetView.as_view()),
    path('reset/password/confirm/<str:uidb64>/<str:token>', views.PasswordResetConfirmView.as_view()),
    path('organisation/action/<int:pk>', views.OrganisationAction.as_view()),
    path('organisation/<int:org_id>/update/<int:admin_id>/', views.edit_organization),
    
    
]
