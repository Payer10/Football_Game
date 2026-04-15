from django.urls import path
from .views import RegisterView, LoginView , UserDetailView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserDetailView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
] + router.urls