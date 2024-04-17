from django.urls import path
from glucose_levels import views


urlpatterns = [
    path('', views.GlucoseLevelList.as_view(), name='glucose_level_list'),
    path('<str:pk>/', views.GlucoseLevelDetail.as_view(), name='glucose_level_detail'),
]