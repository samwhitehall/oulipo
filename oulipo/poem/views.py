from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from poem.serializers import PoemModelSerializer


class PoemViewSet(ViewSet):
    serializer_class = PoemModelSerializer

    def create(self, request):
        serialized = PoemModelSerializer(request.data)
        return Response(serialized.data)
