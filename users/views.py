from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterSerializer, UserSerializer
from .models import Role
from tasks.permissions import IsAdmin

# -----------------------------------
# REGISTER USER
# -----------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Default role
        Role.objects.create(user=user, role="Employee")

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User registered successfully!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": "Employee"
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# -----------------------------------
# LOGIN USER
# -----------------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid username or password"}, status=400)

        refresh = RefreshToken.for_user(user)
        role = getattr(user.role, 'role', None)

        return Response({
            "message": "Login successful!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": role
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)

# -----------------------------------
# ASSIGN ROLE (Admin only)
# -----------------------------------
class AssignRoleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        new_role = request.data.get("role")

        if new_role not in ["Admin", "Manager", "Employee"]:
            return Response({"error": "Invalid role"}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        role_obj, created = Role.objects.get_or_create(user=user)
        role_obj.role = new_role
        role_obj.save()

        return Response({"message": f"Role updated to {new_role}"}, status=200)
