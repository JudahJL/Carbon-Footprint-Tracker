from django.urls import path

import footprint.views

urlpatterns = [
    path('', footprint.views.home, name='home'),
    path('index/', view=footprint.views.index, name='index'),
    path('register/', footprint.views.register, name='register'),
    path('login/', footprint.views.user_login, name='login'),
    path('logout/', footprint.views.user_logout, name='logout'),
    path("dashboard/", footprint.views.dashboard, name="dashboard"),
    path("delete/<int:pk>/", footprint.views.delete_footprint_json, name="delete_footprint"),
]
