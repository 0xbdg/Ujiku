from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r"accounts", AccountViewAPI, basename="account-api")

urlpatterns = router.urls
