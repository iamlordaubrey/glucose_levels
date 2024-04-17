from django.urls import path
from glucose_levels import views


urlpatterns = [
    path('', views.GlucoseLevelList.as_view())
]