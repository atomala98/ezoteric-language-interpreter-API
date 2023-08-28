from django.urls import include, path
from rest_framework import routers
from application import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('user/', views.user_endpoint_list),
    path('user/<int:pk>/', views.user_endpoint_detail),
    path('brainfuck/', views.brainfuck_endpoint_list),
    path('brainfuck/<int:pk>/', views.brainfuck_endpoint_detail),
    path('befunge/', views.befunge_endpoint_list),
    path('befunge/<int:pk>/', views.befunge_endpoint_detailed),
    path('whitespace/', views.whitespace_endpoint_list),
    path('whitespace/<int:pk>/', views.whitespace_endpoint_detailed),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]