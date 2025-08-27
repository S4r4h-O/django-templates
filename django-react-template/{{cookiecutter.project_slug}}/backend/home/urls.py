from django.urls import path
from .views import HomepageView

urlpatterns = [
    path("api/homepage/", HomepageView.as_view(), name="homepage"),
]
