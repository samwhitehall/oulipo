# TODO: validation
# TODO: deserialization
from rest_framework import serializers

from poem.common import CATEGORIES, TAGS
from poem.models.words import Poem


class TokenSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=CATEGORIES)
    content = serializers.CharField(
        trim_whitespace=False, allow_blank=True, required=False)
    original_word = serializers.CharField(
        required=False, trim_whitespace=False)
    tag = serializers.ChoiceField(choices=TAGS, required=False)


class OptionsSerializer(serializers.Serializer):
    advance_by__noun = serializers.IntegerField(required=False)
    advance_by__verb = serializers.IntegerField(required=False)
    # TODO: advanced options


class PoemModelSerializer(serializers.Serializer):
    title = serializers.CharField(trim_whitespace=False, allow_blank=True)
    raw_text = serializers.CharField(trim_whitespace=False, allow_blank=True)
    options = OptionsSerializer()
    tokens = TokenSerializer(required=False, many=True)
    # TODO: add links

    def create(self, validated_data):
        return Poem(**validated_data)
