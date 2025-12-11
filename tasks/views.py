from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from users.models import Role

def get_role(user):
    return getattr(user.role, 'role', None)

# -----------------------------------
# LIST + CREATE TASKS
# -----------------------------------
class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = get_role(request.user)
        if role in ["Admin", "Manager"]:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        role = get_role(request.user)
        if role not in ["Admin", "Manager"]:
            return Response({"error": "Not allowed"}, status=403)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# -----------------------------------
# TASK DETAIL / UPDATE / DELETE
# -----------------------------------
class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_task(self, id):
        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist:
            return None

    def get(self, request, id):
        task = self.get_task(id)
        if not task:
            return Response({"error": "Task not found"}, status=404)

        role = get_role(request.user)
        if role != "Admin" and role != "Manager" and task.owner != request.user:
            return Response({"error": "Not allowed"}, status=403)

        serializer = TaskSerializer(task)
        return Response(serializer.data)


    def patch(self, request, id):
        task = self.get_task(id)
        if not task:
            return Response({"error": "Task not found"}, status=404)

        role = get_role(request.user)
        if role == "Employee" and task.owner != request.user:
            return Response({"error": "Not allowed"}, status=403)

        if 'is_completed' in request.data:
            task.is_completed = request.data['is_completed']
            task.save()

        serializer = TaskSerializer(task)
        return Response(serializer.data)


    def delete(self, request, id):
        task = self.get_task(id)
        if not task:
            return Response({"error": "Task not found"}, status=404)

        role = get_role(request.user)
        # Allow Admin to delete any task, Employee only their own
        if role != "Admin" and task.owner != request.user:
            return Response({"error": "Not allowed"}, status=403)

        task.delete()
        return Response({"message": "Task deleted successfully"}, status=200)
