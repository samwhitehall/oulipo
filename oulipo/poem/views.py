from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from poem.models.words import Poem
from poem.serializers import PoemModelSerializer


class PoemViewSet(ViewSet):
    serializer_class = PoemModelSerializer

    def create(self, request):
        serializer = PoemModelSerializer(data=request.data)
        if serializer.is_valid():
            poem_model = serializer.save()

            # TODO: do we need this twice?
            update_serializer = PoemModelSerializer(poem_model)
            return Response(update_serializer.data)

        else:
            # TODO: return more than bare status code
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Poem.objects.all()
        saved_poem = get_object_or_404(queryset, slug=pk)

        # TODO: get options from URL
        poem = Poem.create(saved_poem.title, saved_poem.raw_text, {})
        serializer = PoemModelSerializer(poem)
        return Response(serializer.data)
