from django.contrib import admin
from django.urls import path, include
from taskmanager import views as page_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # API URLs
    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),

    # Frontend pages
    path('', page_views.homepage, name='homepage'),
    path('register/', page_views.register_page, name='register_page'),
    path('tasks-page/', page_views.tasks_page, name='tasks_page'),
]
