from django.urls import path
from . import views
from .views import (PostListView)

urlpatterns = [
    path('', PostListView.as_view(),name='qgen-home'),
    path('mcqsteps/', views.mcqview,name='mcq-gen'),
    path('summary/',views.summaryview,name='summary-gen'),

]

