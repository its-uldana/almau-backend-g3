from django.urls import path
from .cbv import ListCreateBlogAPIView, RetrieveUpdateDestroyAPIView
#from .fbv import list_create_blog
urlpatterns = [
    path('blogs', ListCreateBlogAPIView.as_view()),
    path('blogs/<int:pk>', RetrieveUpdateDestroyAPIView.as_view())
]