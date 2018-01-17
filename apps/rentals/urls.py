from django.conf.urls import url, include
#from utils.views import ResetPasswordViewSet, ChangePasswordViewSet
from base.views import Index
from rentals.views import NewRentalView, RentalDetailView, RentalDeleteView

urlpatterns = [
    url(r'^new-rental/$', NewRentalView.as_view(), name = "new-rental"),
    url(r'^rental-detail/(?P<pk>\d+)/$', RentalDetailView.as_view(), name = "rental-detail"),
    url(r'^rental-delete/(?P<pk>\d+)/$', RentalDeleteView.as_view(), name = "rental-delete"),
]
