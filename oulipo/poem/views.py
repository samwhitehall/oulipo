from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from poem.models.words import Poem
from poem.serializers import PoemModelSerializer


# TODO: rename this
def create_body(request):
    serializer = PoemModelSerializer(data=request.data)
    if serializer.is_valid():
        poem_model = serializer.save()

        # TODO: do we need this twice?
        update_serializer = PoemModelSerializer(poem_model)
        return Response(update_serializer.data)

    else:
        # TODO: return more than bare status code
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create(request):
    return create_body(request)


def retrieve(request, slug):
    queryset = Poem.objects.all()
    saved_poem = get_object_or_404(queryset, slug=slug)

    # TODO: get options from URL
    poem = Poem.create(saved_poem.title, saved_poem.raw_text, {}, slug=slug)
    serializer = PoemModelSerializer(poem)
    return Response(serializer.data)


def update(request, slug):
    response = create_body(request)
    return response


@api_view(['GET', 'PUT'])
def poem_view(request, slug):
    handler = {
        'GET': retrieve,
        'PUT': update,
    }

    return handler[request.method](request, slug)
