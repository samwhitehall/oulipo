from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, 
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.viewsets import ViewSet

from poem.serializers import PoemModelSerializer


class PoemViewSet(ViewSet):
    serializer_class = PoemModelSerializer

    def create(self, request):
        serializer = PoemModelSerializer(data=request.data)
        if serializer.is_valid():
            try:
                poem_model = serializer.save()
            except Exception as e:
                data = {'errors': [e.message]}
                return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR) 

            update_serializer = PoemModelSerializer(poem_model)
            return Response(update_serializer.data)

        else:
            data = {'errors': serializer.errors}
            return Response(data, status=HTTP_400_BAD_REQUEST)
