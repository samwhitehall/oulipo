from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from poem.serializers import PoemModelSerializer


class PoemViewSet(ViewSet):
    serializer_class = PoemModelSerializer

    def create(self, request):
        serializer = PoemModelSerializer(data=request.data)
        serializer.is_valid()

        serializer.save()
        json_response = JSONRenderer().render(serializer.data)

        return Response(json_response)
