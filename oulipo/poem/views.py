from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from poem.serializers import PoemModelSerializer


class PoemViewSet(ViewSet):
    serializer_class = PoemModelSerializer

    def create(self, request):
        serializer = PoemModelSerializer(data=request.data)
        if serializer.is_valid():
            poem_model = serializer.save()

            update_serializer = PoemModelSerializer(poem_model)
            return Response(update_serializer.data)

        else:
            # TODO: return more than bare status code
            return Response(status=status.HTTP_400_BAD_REQUEST)
