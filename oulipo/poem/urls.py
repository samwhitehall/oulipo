from rest_framework import routers

from poem.views import PoemViewSet

router = routers.SimpleRouter()
router.register(r'poem', PoemViewSet, base_name='poem')

urlpatterns = router.urls
