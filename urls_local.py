from django.urls import include, path

urlpatterns = [
    path('', include('app_manager.urls')),
]
