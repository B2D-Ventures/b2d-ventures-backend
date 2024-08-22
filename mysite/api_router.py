from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from b2d_ventures.app.views import AuthViewSet, AdminViewSet

if settings.DEBUG:
  router = DefaultRouter()
else:
  router = SimpleRouter()

router.register("auths", AuthViewSet, basename="auth")
router.register("admin", AdminViewSet, basename="admin")

app_name = "api"
urlpatterns = router.urls
