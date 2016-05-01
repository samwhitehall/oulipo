# TODO: validation
# TODO: deserialization
from rest_framework import serializers

from poem.common import CATEGORIES
from poem.models.words import Poem


class TokenSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=CATEGORIES)
    content = serializers.CharField(
        trim_whitespace=False, allow_blank=True, required=False)
    original_word = serializers.CharField(required=False)


class OptionsSerializer(serializers.Serializer):
    advance_by = serializers.DictField(child=serializers.IntegerField())
    # TODO: advanced options


class PoemModelSerializer(serializers.Serializer):
    raw_text = serializers.CharField(trim_whitespace=False, allow_blank=True)
    options = OptionsSerializer()
    tokens = TokenSerializer(required=False, many=True)
    # TODO: add links

    def create(self, validated_data):
        return Poem(**validated_data)
