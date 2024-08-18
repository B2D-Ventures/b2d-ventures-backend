from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from b2d_ventures.app.views import AuthViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("auths", AuthViewSet, basename="auth")

app_name = "api"

urlpatterns = router.urls
