
from django.urls import path

from sandbox import views


urlpatterns = [
    path('/data/item/<int:item_id>/', views.CacheItemDataView.as_view(), name="cached_view"),
    path("/restricted-area/", views.RestrictedPathView.as_view(), name="restricted_path"),
    path("/normalize-user/", views.JsonNormalizeView.as_view()),
    path("/device-routing/", views.DeviceRoutingView.as_view()),
    path("/get-value/", views.DataGetView.as_view()),
    path("/update-value/<str:key>/<value>/", views.DataUpdateView.as_view()),
]