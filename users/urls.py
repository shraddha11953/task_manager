


from django.urls import path
from .views import RegisterView, LoginView, AssignRoleView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("assign-role/", AssignRoleView.as_view(), name="assign-role"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
