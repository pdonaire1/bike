from django.conf.urls import url, include
#from utils.views import ResetPasswordViewSet, ChangePasswordViewSet
from base.views import Index
from .views import *

urlpatterns = [
    url(r'^$', Index.as_view(), name = "index"),
    url(r'^login$', LoginView.as_view(), name = "login"),
    url(r'^logout$', LogoutView.as_view(), name = "logout"),
]
