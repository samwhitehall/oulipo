from rest_framework import routers

from poem.views import PoemViewSet

router = routers.SimpleRouter()
router.register(r'poems', PoemViewSet, base_name='poems')

urlpatterns = router.urls
