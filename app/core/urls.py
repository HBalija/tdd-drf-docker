from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('create/', views.CreateuserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('edit/', views.ManageUserView.as_view(), name='detail')
]
