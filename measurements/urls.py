##for measurements

from django.urls import path

from .views import *

urlpatterns=[
    path('',calculate_distance_view,name="calculate-view"),

    ]
