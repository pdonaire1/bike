from django.conf.urls import url, include
#from utils.views import ResetPasswordViewSet, ChangePasswordViewSet
from base.views import Index
from rentals.views import NewRentalView

urlpatterns = [
    url(r'^new-rental$', NewRentalView.as_view(), name = "new-rental"),
]
